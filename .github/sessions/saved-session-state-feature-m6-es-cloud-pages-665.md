# Session pointer: M6.P2 T18, EmulationStation's cloud pages, cards and text, with their unit tests (#665)

> **Seeded:** 2026-10-26 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch (distribution):** `feature/m6-es-cloud-pages-665`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch and `docs/reviews/{order.md,slices.json,inventory.json,status.md}`); the coordinator's tip merged in (`7769e792a4` at `4db784d1c0`, one merge, carrying the brief's versions 1 and 2, the register rows the brief cites, the day's logs)
> **Worktree (distribution):** `/workspace/repos/pixelelated/distribution.worktrees/m6-es-cloud-pages-665` -- the audit artifacts, the work log, this pointer and every ceremony live here
> **Worktree (EmulationStation):** `/home/max/Development/emulationstation-next.worktrees/m6-es-cloud-pages-665`, branch `feature/m6-es-cloud-pages-665`, cut by the coordinator from **the pin `16dbac5211eea7e70db7394372033be2be7df829`** (what `projects/ROCKNIX/packages/ui/emulationstation/package.mk`'s `PKG_VERSION` names at `8ebaf8daad`); the sources are read and the fixes are made here, on this branch only; **the pin bump in the distribution is the coordinator's**
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, no path of theirs named in a run, **no M7 build root read**; the other ES checkouts under `~/Development/emulationstation-next.worktrees/` (the `m7-*` ones M7's) are read with `git -C ... show` only, never checked out or written; M7's October work on these files is cited by issue number
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, the session the dispatch comment on #665 names (`m6-t5-build-engine`)
> **Epic:** #700 (the interface: T2 accepted and closed out; this slice; T20, T21, T26, T31 to T37, T44 after); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Extended -- **two seats, GPT-6 Astra at `max` then Gemini 4 Argon at `high`** over a trimmed, scanned packet (D-WORKFLOW-195: trim before any seat sees it; T17's first packet was 437 KB and Argon fails at that size), a probe then one refutation each; `review-plan.json` records depth `extended`, two reviewers; **exactly four keyed invokes**, every other `tools/council/run` call with `COUNCIL_ENV_FILE=/nonexistent`; every scan hit dispositioned by shape, a value stops the packet; a test fixture's secret-shaped literal is itself a finding (#1061)
> **The lens:** brittleness and new functionality over the 30 fork-own files at the pin (11,193 lines, every one read; eight sources, 22 test files): the card (`ThreadedCloudSync`), the job (`CloudTransferJob`), the page (`GuiCloudTransfer`) and the pure text (`CloudText`) -- a library whose callers (`GuiMenu.cpp`, `main.cpp`, `FileData.cpp`, `ProxyCards.cpp`) are other slices'. Q3 in three families: the protocol under a pipe; lifetimes and threads; the words. Two generated tables (§ The protocol, § The why table). **The fallback map's drift is in the rule and the header comment, not the code.**
> **The rule:** **the lane changes nothing under the distribution's `packages/`, `projects/` or `tools/` at any stage, and nothing in the ES worktree outside the 30 at stages A to D**; a defect is a `bug` with its trace and `Already written:` line, fixed only under a stream brief the coordinator writes, on the ES branch, proven twice (`fix-unit-test` or `fix-walk-pending-image`), `tools/es-syntax-check` PASS where a toolchain exists, else the host `g++ -fsyntax-only` pass or its `CANNOT` with the missing header named (the brief's § 5: the host has no toolchain, #1137), and a clean non-ASCII comment grep before its commit; **every ES change keeps its flow and screenshot evidence** (D-WORKFLOW-155/156, D-UI-039: `docs/es-menu-map.md` § Cloud in the same change); **nothing on a person's device or cloud** (D-QA-015); **`rm -rf` only as `"${VAR:?}"/...` or a literal path, in its own short command, never inside a `bash -c` script**
> **The host:** M6's and M7's by the shared log `/tmp/m7-m6-host-coordination-20261023.txt` (M7 writes timestamped lines, not `== ` blocks: read the whole tail); this slice runs **one guest window**, asked for on #665 with its plan after stage B and granted in the host file's queue: one GENERIC_X64 guest from M6's `069fc2704421` copy, the QA WebDAV on the lane's isolation under `/workspace/tmp/m6-t18/`, 30 minutes from START; **the post contract**: `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` in the post's first line; stop by pidfile, the leftover check, every output kept; **the installed EmulationStation identified against the pin before any verdict**; the disk retired with its path, size and sha in `00`
> **Register:** the rows this brief cites are on the coordinator's branch, merged here; D-CLOUD-185 the highest cloud row and D-WORKFLOW-209 the highest workflow row (D-WORKFLOW-188 on the P1 branch only); a row this slice forces (none expected) takes an ID the coordinator assigns on #665
> **The brief:** `docs/reviews/briefs/es-cloud-pages.md` at `99515f83ad` (version 2, after a stranger's proof of version 1 -- its corrections listed at its end); #665's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

Not started. The first commit on the distribution branch is the running
log's header (the model, the effort, `reviewed-at` the distribution HEAD with
the pin beside it, the host file's last lines, the census),
`01-research-notes.md` § Scope (the block of brief § 2 with its output and
the § 5 runs' figures), this pointer updated, and the day's work-log entry
headed `#665` (prose through a quoted heredoc or the Write tool). The ES
worktree stays at the pin until stage E. `.qa-scratch/` is gitignored and
`git status --short` is read before every `git add -A`. No network is used
except the seats' four keyed invokes.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-cloud-pages-665
cd "$D"   # no fetch of any kind: 651150fc88 and c445081a59 are already in the repository
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                     # empty
test -f docs/reviews/inventory.json && echo inventory
grep -c 'D-CLOUD-185' docs/decision-register.md                                    # 1 or more: the coordinator's tip is merged
W=/home/max/Development/emulationstation-next.worktrees/m6-es-cloud-pages-665
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l                      # the pin; 0
tail -n 6 /tmp/m7-m6-host-coordination-20261023.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
sed -n '1,170p' docs/reviews/briefs/es-cloud-pages.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets, T5, T6, T7, T8, T23, T40, T11, T27, T25, T28, T9, T10, T12,
T13, T22, T14, T15, T45, T16, T29, T17, **then this branch, with the pin
moved to the ES branch's tip in the same integration commit**, then T4's
last. When `next` moves, the **coordinator** merges `next` into this branch,
and never between stage A and stage D; the coordinator merges its own
branch into this one at hand-back, before the last criterion's checkers run.
Never merge another lane's feature branch here, in either repository. Every
lane and the M7 lane append to `docs/decision-register.md`, the day's work
log and `docs/work-logs/INDEX.md`: keep every append, regenerate the index,
never edit another lane's rows; a merge with conflicts is checked for
leftover markers before it is committed (#696), and a union of two ledgers
is made by whole entries. Nothing here builds an image, touches a device, a
cloud account, a provider, a key file, the host's swap, another lane's
worktree, or a guest outside the one granted window.

## Checkpoints

- (none yet; the executor appends one line per stage: the stage, both tips, the time)
