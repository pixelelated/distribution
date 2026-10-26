# Session pointer: M6.P2 T21, EmulationStation's state primitives and its bridge to the OS (#668)

> **Seeded:** 2026-10-26 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch (distribution):** `feature/m6-es-state-and-bridge-668`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch and `docs/reviews/{order.md,slices.json,inventory.json,status.md}`); the coordinator's tip merged in (`7d4c4f65f7` at `66aa8aff80`, one merge, carrying the brief's versions 1 and 2, the register rows the brief cites, the day's logs)
> **Worktree (distribution):** `/workspace/repos/pixelelated/distribution.worktrees/m6-es-state-and-bridge-668` -- the audit artifacts, the work log, this pointer and every ceremony live here
> **Worktree (EmulationStation):** `/home/max/Development/emulationstation-next.worktrees/m6-es-state-and-bridge-668`, branch `feature/m6-es-state-and-bridge-668`, cut by the coordinator from **the pin `16dbac5211eea7e70db7394372033be2be7df829`** (what `projects/ROCKNIX/packages/ui/emulationstation/package.mk`'s `PKG_VERSION` names at `8ebaf8daad`); the sources are read and the fixes are made here, on this branch only; **the pin bump in the distribution is the coordinator's**
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, no path of theirs named in a run, **no M7 build root read**; the other ES checkouts under `~/Development/emulationstation-next.worktrees/` (the `m7-*` ones M7's, `qa-integration` another lane's) are read with `git -C ... show` only, never checked out or written; M7's October work on these files is cited by issue number
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, the session the dispatch comment on #668 names (`m6-t5-build-engine`)
> **Epic:** #700 (the interface: T2 and T18 accepted and closed out; T20 #667 briefed; this slice; T26, T31 to T37, T44 after); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Extended -- **two seats, GPT-6 Astra at `max` then Gemini 4 Argon at `high`** over a trimmed, scanned packet (D-WORKFLOW-195: trim before any seat sees it; T17's first packet was 437 KB and Argon fails at that size), a probe then one refutation each; `review-plan.json` records depth `extended`, two reviewers; **exactly four keyed invokes**, every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`; these files name the Wi-Fi key, the scraper's pair and account and the RetroAchievements keys by setting name, so every scan hit is dispositioned by shape in the manifest, and a value stops the packet; a test fixture's secret-shaped literal is itself a finding (#1061)
> **The lens:** security and state preservation over 14 paths at the pin (9,249 lines, all read): the shell bridge (`ApiSystem.*`: four executors, eleven exit reads without `WIFEXITED`, two quoting rules), the network client (`HttpReq.*`: one `curl_multi` driven by whichever thread calls it; #1154 cited), the two stores and the fork's atomic writer (`Settings.*`, `SystemConf.*`, `AtomicFileUtil.*`: one locked and recorded, one not), the Wi-Fi page and the scraper's credentials (`GuiWifi.*`, `ScreenScraper.*`). Q1 to Q8 in four families: a command built from a player's string; a credential's sink; a state write that can lose the record; a check whose failure reads as success
> **The rule:** **the lane changes nothing under the distribution's `packages/`, `projects/` or `tools/` at any stage** -- the OS-side writers of `system.cfg` (`001-functions`, `chksysconfig`, `post-update`, `wifictl`, `setsettings.sh`) are T1's files, and a defect there is a punch item for the coordinator's ruling at the pause -- **and nothing in the ES worktree outside the 14 at stages A to D**; a defect is a `bug` with its trace and `Already written:` line, fixed only under a stream brief the coordinator writes, on the ES branch, proven twice (`fix-unit-test` or `fix-walk-pending-image`), `tools/es-syntax-check` PASS where a toolchain exists, else the host `g++ -fsyntax-only` pass or its `CANNOT` with the missing header named (#1137), and a clean non-ASCII comment grep before its commit; the unit tests built by the generated `g++` command before every commit; a fixture rewrites no path and runs in a bubblewrap sandbox started with `--clearenv`; the walks' steps under the audit folder's `stage-e/walks/`; the pin is not moved by the lane
> **The host:** M6's and M7's by the shared log `/tmp/m7-m6-host-coordination-20261023.txt` (M7 writes timestamped lines, not `== ` blocks: read the whole tail); this slice runs **one guest window**, asked for on #668 with its plan and bound after stage B and granted in the host file's queue: one GENERIC_X64 guest from M6's `069fc2704421` copy at `/workspace/artifacts/m6-t2-20261023/`, started at 640x480 (`generic-x64-vm run --res`; `vm-pair` has no option, #1141), the post contract `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` as each post's first line with the census, the stop by pidfile at bound plus grace, the disk retired after with path, size and sha; the modes of both stores, their copies, the cookie jar and the NetworkManager keyfile after a join driven by `tools/cloud-input-test`'s fake networks, the recovery ladder on the image for both stores with the player's frame, the Wi-Fi key on argv as a masked count, the `7z` positive on a scratch library, the #1154 positive against a host-run TLS endpoint; **the QA ScreenScraper account only** (`tools/qa-accounts`, never printed; D-QA-016), never the owner's (D-QA-015), for the one sign-in the brief's § 5 names, last
> **Register:** the rows this brief cites are on the coordinator's branch, merged here; D-CLOUD-185 the highest cloud row and D-WORKFLOW-209 the highest workflow row (D-WORKFLOW-188 on the P1 branch only); a row this slice forces (none expected) takes an ID the coordinator assigns on #668
> **The brief:** `docs/reviews/briefs/es-state-and-bridge.md` at `2f1d006461` (version 2, after a stranger's proof of version 1 -- its corrections listed at its end); #668's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**Stage A done (2026-10-26 21:00 UTC); stage B next.**

- **Stage A:**
  - the first commands, § 2's block and § 5's runs all at the brief's figures, with two deltas from its comments (`wifictl`'s 195/209 outside the pattern; 25 `writeAllText` call sites of 27 lines);
  - the unit tests built at the pin by `tools/t21-build-tests.sh` (221 cases, the eight files 80), with rapidjson from the recipe's own tarball and four patches;
  - `tests/wifi-profile-lifetime.py` PASS;
  - T20's PL-08 fixture and S2's `HttpReqOptions` field read by `git show`.
- **Records:** `00` at `reviewed-at` `4844a773ca` beside the pin; `01` § Scope.
- **Next, stage B:**
  - read the 14 whole, and § 3's remaining rules, map lines, blindspots and audits;
  - write `02` with its sections, the generators for § The commands and § The writers asserting their counts, and the host positives (the kill-the-writer fixture for both stores and the shell writers, the seed-before-the-record case);
  - then the window request on #668 with its plan and its bound.
- **What runs here:** nothing. Scratch is `/workspace/tmp/m6-t21/` (`rj/`, `build/pin/`, `stageA/`).

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-state-and-bridge-668
cd "$D"   # no fetch of any kind: 651150fc88 and c445081a59 are already in the repository
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                     # empty
test -f docs/reviews/inventory.json && echo inventory
grep -c 'D-CLOUD-185' docs/decision-register.md                                    # 1 or more: the coordinator's tip is merged
W=/home/max/Development/emulationstation-next.worktrees/m6-es-state-and-bridge-668
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l                      # the pin; 0
tail -n 6 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
sed -n '1,160p' docs/reviews/briefs/es-state-and-bridge.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets, T5, T6, T7, T8, T23, T40, T11, T27, T25, T28, T9, T10, T12,
T13, T22, T14, T15, T45, T16, T29, T17, T18, T19, T20, **then this branch,
with the pin moved to the ES branch's tip in the same integration commit**,
then T4's last. When `next` moves, the **coordinator** merges `next` into
this branch, and never between stage A and stage D; the coordinator merges
its own branch into this one at hand-back, before the last criterion's
checkers run. Never merge another lane's feature branch here, in either
repository. Every lane and the M7 lane append to `docs/decision-register.md`,
the day's work log and `docs/work-logs/INDEX.md`: keep every append,
regenerate the index, never edit another lane's rows; a merge with conflicts
is checked for leftover markers before it is committed (#696), and a union
of two ledgers is made by whole entries. Nothing here builds an image,
touches a device, a cloud account, a provider, a key file, the host's swap,
another lane's worktree, or a guest outside the one granted window.

## Checkpoints

- Stage A, 21:00 UTC: distribution `4844a773ca` + stage A's commit; ES at the pin `16dbac5211` (unchanged).
- (none yet; the executor appends one line per stage: the stage, both tips, the time)
