# Session pointer: M6.P2 T26, EmulationStation's main menu, GuiMenu (#673)

> **Seeded:** 2026-10-26 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch (distribution):** `feature/m6-es-guimenu-673`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch and `docs/reviews/{order.md,slices.json,inventory.json,status.md}`); the coordinator's tip merged in (`a33c7ba061` at `8c6789f2c2`, one merge, carrying the brief's versions 1 and 2, the register rows the brief cites, the day's logs)
> **Worktree (distribution):** `/workspace/repos/pixelelated/distribution.worktrees/m6-es-guimenu-673` -- the audit artifacts, the work log, this pointer and every ceremony live here
> **Worktree (EmulationStation):** `/home/max/Development/emulationstation-next.worktrees/m6-es-guimenu-673`, branch `feature/m6-es-guimenu-673`, cut by the coordinator from **the pin `16dbac5211eea7e70db7394372033be2be7df829`** (what `projects/ROCKNIX/packages/ui/emulationstation/package.mk`'s `PKG_VERSION` names at `8ebaf8daad`); the sources are read and the fixes are made here, on this branch only; **the pin bump in the distribution is the coordinator's**
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, no path of theirs named in a run, **no M7 build root read**; the other ES checkouts under `~/Development/emulationstation-next.worktrees/` (the `m7-*` ones M7's, `qa-integration` another lane's) are read with `git -C ... show` only, never checked out or written; M7's October work on this file is cited by issue number
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, the session the dispatch comment on #673 names (`m6-t5-build-engine`)
> **Epic:** #700 (the interface: T2 and T18 accepted and closed out; T20 #667 and T21 #668 briefed; this slice; T31 to T37, T44 after); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Independent -- **one seat, GPT-6 Astra at `max`** over a trimmed, scanned packet (D-WORKFLOW-195: one file of 11,747 lines is most of the packet; trim the upstream regions the lens does not reach and say so in the manifest), a probe then one refutation; `review-plan.json` records depth `independent`, one reviewer; **exactly two keyed invokes**, every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`; every scan hit dispositioned by shape, a value stops the packet; a test fixture's secret-shaped literal is itself a finding (#1061)
> **The lens:** new functionality and brittleness over two files at the pin (11,883 lines, both read whole, both rewritten from ROCKNIX's base: 5,124 insertions over 225 fork commits): every fork page is built in this file and reached from it -- the cloud setup wizard and its transitions, the cloud hub, the network and Wi-Fi pages, the relink page, the save rows, the RetroAchievements rows -- beside upstream's pages read for brittleness and left as upstream has them (D-UI-079). Q1 to Q7 in the families the brief names
> **The rule:** **the lane changes nothing under the distribution's `packages/`, `projects/` or `tools/` at any stage, and nothing in the ES worktree outside the two files at stages A to D**; a defect is a `bug` with its trace and `Already written:` line, fixed only under a stream brief the coordinator writes, on the ES branch, proven twice (`fix-unit-test` or `fix-walk-pending-image`), `tools/es-syntax-check` PASS where a toolchain exists, else the host `g++ -fsyntax-only` pass or its `CANNOT` with the missing header named (#1137), a clean non-ASCII comment grep before its commit, and **`docs/es-menu-map.md` updated in the same commit as any row added, moved or renamed, `tools/es-menu-map-check` passing (D-UI-039)**; the walks' steps under the audit folder's `stage-e/walks/`; the pin is not moved by the lane
> **The host:** M6's and M7's by the shared log `/tmp/m7-m6-host-coordination-20261023.txt` (M7 writes timestamped lines, not `== ` blocks: read the whole tail); this slice runs **one guest window**, asked for on #673 with its plan and bound after stage B and granted in the host file's queue: one GENERIC_X64 guest from M6's `069fc2704421` copy at `/workspace/artifacts/m6-t2-20261023/`, started at 640x480 (`generic-x64-vm run --res`; `vm-pair` has no option, #1141), the post contract `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` as each post's first line with the census, the stop by pidfile at bound plus grace, the disk retired after with path, size and sha; the fork pages' walks with their strings read back, the wizard's transitions, the confirmations' back-button landing, the rows' stores read from both files after a page close; **the QA accounts only** (`tools/qa-accounts`, never printed; D-QA-016), never the owner's (D-QA-015)
> **Register:** the rows this brief cites are on the coordinator's branch, merged here; D-WORKFLOW-209 the highest workflow row and D-RA-050 the highest row (D-WORKFLOW-188 on the P1 branch only); a row this slice forces (none expected) takes an ID the coordinator assigns on #673
> **The brief:** `docs/reviews/briefs/es-guimenu.md` at `4b0ee281b5` (version 2, after a stranger's proof of version 1 -- its corrections listed at its end); #673's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**Stage E: the streams, serial, on the ES branch** (the ruling 09:17 UTC, #673 comment 6438068860; the stream brief `docs/reviews/briefs/t26-streams.md` at `4bd066551a`).

- **The bugs:** #1215 to #1233 filed (`stage-e/bugs-filed.txt`).
- **Done:** S1 (PL-01, #1215) at ES `70a00ad13`; S2 (PL-02, #1216; PL-15) at ES `03183f899`, the map at `190faf95fe`; S3 (PL-03 #1217, PL-04 #1218) at ES `d9bcdfb8a` and `2b50bf112` (its test's loads); S4 (PL-05, #1219) at ES `e96222310`; S5 (PL-06, #1220) at ES `b7de744aa`.
- **Next:** S6 (PL-07 #1221, PL-08 #1222), then S7 to S13 in order; each with `stage-e/sN-before.txt`, `sN-after.txt`, `sN-checks.txt` (`bash stage-e/checks.sh SN`), one ES commit, `.githooks/pre-push-test`, the push; then `02` § The streams via `stage-b/02-template.md` and `tools/t26-assemble-02.py`.
- **Scratch:** `/workspace/tmp/m6-t26/` (the pin's files in `tmp/`, the recipe's patched rapidjson in `rapidjson/`).

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-guimenu-673
cd "$D"   # no fetch of any kind: 651150fc88 and c445081a59 are already in the repository
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                     # empty
test -f docs/reviews/inventory.json && echo inventory
grep -c 'D-RA-050' docs/decision-register.md                                       # 1 or more: the coordinator's tip is merged
W=/home/max/Development/emulationstation-next.worktrees/m6-es-guimenu-673
git -C "$W" log --oneline 16dbac5211..HEAD; git -C "$W" status --short | wc -l   # one commit per stream done; 0
tail -n 6 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
sed -n '1,150p' docs/reviews/briefs/es-guimenu.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets, T5, T6, T7, T8, T23, T40, T11, T27, T25, T28, T9, T10, T12,
T13, T22, T14, T15, T45, T16, T29, T17, T18, T19, T20, T21, **then this
branch, with the pin moved to the ES branch's tip in the same integration
commit**, then T4's last. When `next` moves, the **coordinator** merges
`next` into this branch, and never between stage A and stage D; the
coordinator merges its own branch into this one at hand-back, before the
last criterion's checkers run. Never merge another lane's feature branch
here, in either repository. Every lane and the M7 lane append to
`docs/decision-register.md`, the day's work log and `docs/work-logs/INDEX.md`:
keep every append, regenerate the index, never edit another lane's rows; a
merge with conflicts is checked for leftover markers before it is committed
(#696), and a union of two ledgers is made by whole entries. Nothing here
builds an image, touches a device, a cloud account, a provider, a key file,
the host's swap, another lane's worktree, or a guest outside the one
granted window.

## Checkpoints

- Stage E, S5, 10:19 UTC: ES `b7de744aa` (pushed); S5's record and `tools/t26-pages.py --listed` on the distribution branch.
- Stage E, S4, 10:06 UTC: ES `e96222310` (pushed); S4's record on the distribution branch.
- Stage E, S3, 09:51 UTC: ES `d9bcdfb8a` (pushed); S3's record on the distribution branch.
- Stage E, S2, 09:42 UTC: ES `03183f899` (pushed); distribution the map `190faf95fe` and S2's record.
- Stage E, S1, 09:27 UTC: ES `70a00ad13` (pushed); the 19 bugs #1215 to #1233.
- Stage D: #1213 filed; the pause posted on #673.
- Stage C, 09:2x UTC: the seat graded, `05` written, the lint PASS.
- The window, 08:31 UTC: RETURN posted; `02` § The guest cycle written.
- Stage B, see the work log: `02` assembled, the window asked for on #673.
- Stage A, 02:50 UTC: distribution `db7be4b104` + stage A's commit; ES at the pin `16dbac5211` (unchanged).
- (none yet; the executor appends one line per stage: the stage, both tips, the time)
