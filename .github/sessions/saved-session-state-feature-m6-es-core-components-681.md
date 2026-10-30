# Session pointer: M6.P2 T34, EmulationStation's core components: the rows, grids, menus, lists, cards, images, videos and text every page is built from (#681)

> **Seeded:** 2026-10-30 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch (distribution):** `feature/m6-es-core-components-681`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch and `docs/reviews/{order.md,slices.json,inventory.json,status.md}`); the coordinator's tip merged in (`200a9a032d` at `00d490e654`, one merge, carrying the brief's versions 1 and 2, the register rows the brief cites, the day's logs)
> **Worktree (distribution):** `/workspace/repos/pixelelated/distribution.worktrees/m6-es-core-components-681` -- the audit artifacts, the work log, this pointer and every ceremony live here
> **Worktree (EmulationStation):** `/home/max/Development/emulationstation-next.worktrees/m6-es-core-components-681`, branch `feature/m6-es-core-components-681`, cut by the coordinator from **the pin `16dbac5211eea7e70db7394372033be2be7df829`** (what `projects/ROCKNIX/packages/ui/emulationstation/package.mk`'s `PKG_VERSION` names at `8ebaf8daad`); the sources are read and the fixes are made here, on this branch only; **the pin bump in the distribution is the coordinator's**
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, no path of theirs named in a run, **no M7 build root read**; the other ES checkouts under `~/Development/emulationstation-next.worktrees/` (the `m7-*` ones M7's, `qa-integration` another lane's, the `m6-*` ones the earlier slices') are read with `git -C ... show` only, never checked out or written; M7's October work on this file is cited by issue number
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, the session the dispatch comment on #681 names (`m6-t3-emulators`)
> **Epic:** #700 (the interface: T2 #649, T18 #665, T20 #667, T21 #668, T26 #673, T31 #678 and T32 #679 accepted, their issues open until the integration moves the pin on `next`; T33 #680 in flight; this slice; T35 #682, T36 #683 and T37 #684 next, T44 after); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Independent -- **one seat, GPT-6 Astra at `max`** over a trimmed, scanned packet (D-WORKFLOW-195: **the 21 fork-modified files whole**, 9,541 lines by the inventory's rule, **and of the 59 upstream-carried files only the ranges the questions cite**; nothing in the 80 is a binary; the expected scan hits are a request-header name, `SDLK_*` constants and identifiers, **every hit dispositioned by name in `packet-manifest.json`** as library plumbing, macro name, identifier or setting name, and a hit that is a value stops the packet; no value goes anywhere), a probe then one refutation; **exactly two keyed `tools/council/run invoke` calls**, every other council call with `COUNCIL_ENV_FILE=/nonexistent`.
> **The lens:** cost against value over the 80 paths of `es-core/src/components/**` at the pin (21,984 lines by `grep -c ''`, 38 `.cpp` and 42 `.h`; the fork modified 21 upstream files, +591/-114 over 33 commits, and added none; 59 byte-identical to ROCKNIX's master; 0 upstream commits on the 80 since the merge base `cada856d86`, so the merge debt is a one-line record, with batocera's eight commits since `1750dded8c` as a reconciliation list for the integration, never a debt figure): the rows, grids, menus, lists, cards, images, videos and text every page is built from; seven questions in the brief's § 4 (the layouts computed from what they last produced and from a moving number; the house constants; input and the help bar; lifetimes; reads and the network; the words; the structure and the merge debt), with the floor's pure leads 3.1 to 3.34 in the brief and the seven that FAIL at the pin first.
> **The rule:** **the lane changes nothing under the distribution's `packages/`, `projects/` or `tools/` at any stage, nothing in the ES worktree at stages A to D (it stays at the pin until stage E), and nothing outside the 80 paths at any stage**; es-core's `guis/`, `Window.cpp`, `ThemeData.cpp`, `GuiComponent.cpp`, `InputConfig.cpp`, `InputManager`, `watchers/`, `Scripting.cpp`, `es-core/CMakeLists.txt` and the rest of es-core are the later es-core slices' (T35's), `resources/` and `utils/` T36's, `HttpReq.*`, `Settings.*`, `SystemConf.*` and `AtomicFileUtil.*` T21's, es-app's files the earlier slices' (`CloudText.*` T18's, `GuiMenu.*` T26's, the other pages T31's, the views and scrapers T32's, the game list and `ScraperSearchComponent` T33's) -- the globs decide; a fix in a neighbour is named for its owner at the pause; the seven accepted lanes' ES tips and T33's (`dd86d7ce20a5` on 2026-10-30; empty inside the 80 at that read) are diffed against the pin inside the 80 at stage A and at the hand-back, and every collision named; a defect is a `bug` with its trace, its `Already written:` line and its VM line (D-WORKFLOW-050, `bugs-are-agent-first.md`); a lead outside the 80 is a Backlog the coordinator files.
> **The host:** M6's and M7's by the shared log `/workspace/tmp/m7-m6-host-coordination.txt` (the durable successor of `/tmp/m7-m6-host-coordination-20261023.txt`, which the reboot of 2026-10-28 removed; M7 writes timestamped lines, not `== ` blocks: read the whole tail); this slice runs **one guest window with two boots**, asked for on #681 with its plan and bound after stage B and granted in the host file's queue: one GENERIC_X64 guest from M6's `069fc2704421` copy at `/workspace/artifacts/m6-t2-20261023/`, started at 640x480 (`generic-x64-vm run --headless --daemonize --res 640x480`; `vm-pair` has no option, #1141) and, for G-11, stopped by pidfile and started again at 1280x800 on the same disk; **30 minutes proposed plus 5 of grace** for a plan of 1,410 s (G-01 to G-12, the brief's § 5 item 2); the post contract `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` as each post's first line with the census (`qemu N, compilers N`), the stop by pidfile at bound plus grace (`tools/vm-stop`, never a pattern), the disk retired after with path, size and sha (D-INFRA-022); the image identified by `BUILD_ID` and file name first and every frame labelled `image` or `pin-binary`; the card's two edges and a pixel over box art, the button bar's gap at both sizes measured by a reader, a dimmed row's luminance, the tab strip's four frames and the reopened page's pair, an OK-only dialog's help bar, a slider's glued suffix, a French page's help bar and its `Unknown help icon` count; the QA accounts only if a row needs one (none does, § 5; `tools/qa-accounts`, never printed; D-QA-016), never the owner's (D-QA-015)
> **Register:** the rows this brief cites are on the coordinator's branch, merged here; D-CLOUD-187 D-INFRA-031 D-LAUNCH-007 D-NET-017 D-QA-063 D-RA-052 D-SYS-014 D-UI-129 D-WORKFLOW-213 are the highest rows of their areas on the coordinator's branch (computed from the decided table at `200a9a032d`), with the ownership row of the brief's § 1 written at dispatch (D-WORKFLOW-188 on the P1 branch only; the merge unites them); the four rows the brief's § 9 expects are put to the coordinator at the pause, never decided by the lane, and a row this slice forces takes an ID the coordinator assigns on #681
> **The brief:** `docs/reviews/briefs/es-core-components.md` at `a6e14fed86` (version 2 of 2026-10-30, after a stranger's proof of version 1 `a728d04c95` -- its corrections listed at its end, `## Corrections in version 2`); #681's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus (20:25 UTC 2026-10-30 update): the stage-D pause

- **Stage C ran:** the guest window (19:28 to 19:39), the packet and its scan, and the seat (two keyed invokes, both PASS). The seat's G-1 to G-16 were each verified at the pin.
- **The pre-issue lint:** PASS with the held reply present; one failure on the committed tree, the reply.
- **The punch list:** 43 items in \`05\` and **#1307** (the audit issue, a sub-issue of #681).
- **The pause** is posted on #681. The lane waits for the coordinator's dispositions and any stream brief.
- **PL-27 is security-sensitive:** the seat's reply is held at \`/workspace/tmp/m6-t34/held/gpt-audit.md\` (mode 600, sha256 \`609c488c...\`). It is never committed or posted until the maintainer names the channel.
- **Owed before or at stage E:** \`tools/t34-build-tests.sh\` and the 34 seam cases, the seven FAIL-at-pin first; the sanitizer cases; the stand-in syntax check over the 37.

## Earlier focus (14:24 UTC 2026-10-30 update): stage A done; stage B next

**Stage A is recorded** in `docs/audits/2026_10_30-epic-m6-es-core-components/`:
- `00-running-log.md`: the header, the eleven keys checked, and the two seeding slips -- this file's line 43, now rewritten, and the Register line's D-SYS-014, which is an open decision; the decided table's highest SYS row is D-SYS-013;
- `01-research-notes.md` § Scope and § The § 5 runs at stage A;
- `stage-a/`: `first-commands.txt`, `membership-block.txt`, `paths.txt`, `runs.txt` and `issue-states.txt`.

Every expectation of § 1, § 2 and § 5 printed as the brief says, with one erratum: the gates command prints 13 lines, which is § 4 Q7's own list. All eight lanes' ES tips are empty inside the 80 (T33's is now `f802c55c62c1`). The ES worktree is at the pin and clean.

**Next is stage B:**
- the brief's § 3 items 2 to 10, read at T34's copies of the rules (six differ from the T3 worktree's);
- then `02-forward-audit.md` in § 6's order;
- then the window request on #681 and in the host file. Per the host file's 09:26 entry, it waits behind M7's TLS proof windows.

No guest, build, fetch or keyed call before the grant.

## Earlier focus (14:46 UTC 2026-10-30 update): stage B done; the window asked for

`02-forward-audit.md` is composed from the nine generators under `tools/` (`tools/t34-02.py <W>` regenerates it). The window plan is `stage-b/window-plan.md`. The window is asked for on #681 and in the host file, and runs only on the coordinator's grant, after every M7 window.

**Next is stage C:**
- the packet, trimmed and scanned;
- the plan and the seat (two keyed invokes only after the grant);
- `tools/t34-build-tests.sh`, with the seven FAIL-at-pin cases first, and the stand-in syntax check over the 37;
- the pre-issue lint.

**Pushing:** `git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push <https URL> <branch>` while the SSH agent is absent.

## Earlier focus (seeded): not started

Not started. Before the first command after `cat`, the eleven keys of this
pointer are read against the brief's § 10 table, and any that names the
predecessor slice is reported on #681 before going on. The first commit on
the distribution branch is the running log's header (the model, the
effort, `reviewed-at` the distribution HEAD with the pin beside it, the
host file's last lines with the time of the read, the census),
`01-research-notes.md` § Scope (the block of brief § 2 with its output and
the § 5 runs' figures), this pointer updated, and the day's work-log entry
headed `#681` (prose through a quoted heredoc or the Write tool). The ES
worktree stays at the pin until stage E. `.qa-scratch/` is gitignored and
`git status --short` is read before every `git add -A`; anything temporary
goes under `/workspace/tmp/m6-t34/`, never `/tmp`. No network is used
except the seat's two keyed invokes.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-core-components-681
cd "$D"   # no fetch of any kind: 651150fc88 and c445081a59 are already in the repository
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git merge-base --is-ancestor 200a9a032d HEAD && echo coordinator-tip-merged
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                     # empty
test -f docs/reviews/inventory.json && echo inventory
/usr/bin/grep -c -E '__[A-Z]+__|\b(CO''HASH|MERGE_''HASH|TIP''HASH|V2''HASH)\b' .github/sessions/saved-session-state-feature-m6-es-core-components-681.md   # 0: the brief's § 9 check; the quotes split each word so this line does not count itself (the seeded line had its hashes filled in and counted 5, stage A)
W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-components-681
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l                      # the pin; 0
git -C "$W" merge-base 16dbac5211eea7e70db7394372033be2be7df829 rocknix/master | cut -c1-10   # cada856d86
date -u +%H:%M:%S; tail -n 6 /workspace/tmp/m7-m6-host-coordination.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
sed -n '1,150p' docs/reviews/briefs/es-core-components.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets, T5, T6, T7, T8, T23, T40, T11, T27, T25, T28, T9, T10, T12,
T13, T22, T14, T15, T45, T16, T29, T17, T18, T19, T20, T21, T33, **then
this branch, with the pin moved to the ES branch's tip in the same
integration commit**, then T35 to T37, then T4's last. When `next` moves,
the **coordinator** merges `next` into this branch, and never between
stage A and stage D; the coordinator merges its own branch into this one
at hand-back, before the last criterion's checkers run. Never merge another
lane's feature branch here, in either repository. Every lane and the M7
lane append to `docs/decision-register.md`, the day's work log and
`docs/work-logs/INDEX.md`: keep every append, regenerate the index, never
edit another lane's rows; a merge with conflicts is checked for leftover
markers before it is committed (#696), and a union of two ledgers is made
by whole entries. Nothing here builds an image, touches a device, a cloud
account, a provider, a key file, the host's swap, another lane's worktree,
or a guest outside the one granted window.

## Checkpoints

- Stage C and D, 20:25 UTC 2026-10-30: the window, the packet, the seat, #1307, the pause; ES `16dbac5211` (the pin, clean).
- Stage B, 14:46 UTC 2026-10-30: 02 composed, the window asked for; ES `16dbac5211` (the pin, clean).
- Stage A, 14:24 UTC 2026-10-30: distribution `22c0d5a2c2` plus the stage-A close commit that carries this line; ES `16dbac5211` (the pin, clean).
