# Session pointer: M6.P2 T35, EmulationStation's window, input, settings and the rest of es-core: the window and its floating surfaces, the input manager and its config file, the es-core dialogs, the theme parser, the script runner, the watchers, the log (#682)

> **Seeded:** 2026-10-31 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch (distribution):** `feature/m6-es-core-window-input-682`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch and `docs/reviews/{order.md,slices.json,inventory.json,status.md}`); the coordinator's tip merged in (`be119338ff` at `b51dd8a805`, one merge, carrying the brief's versions 1 and 2, the register rows the brief cites, the day's logs); the lane's own tip is `b51dd8a805` (at stage A it is `b51dd8a805`)
> **Worktree (distribution):** `/workspace/repos/pixelelated/distribution.worktrees/m6-es-core-window-input-682` -- the audit artifacts, the work log, this pointer and every ceremony live here
> **Worktree (EmulationStation):** `/home/max/Development/emulationstation-next.worktrees/m6-es-core-window-input-682`, branch `feature/m6-es-core-window-input-682`, cut by the coordinator from **the pin `16dbac5211eea7e70db7394372033be2be7df829`** (what `projects/ROCKNIX/packages/ui/emulationstation/package.mk`'s `PKG_VERSION` names at `8ebaf8daad`); the sources are read and the fixes are made here, on this branch only, and nothing is written here before stage E; **the pin bump in the distribution is the coordinator's**
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, no path of theirs named in a run, **no M7 build root read**; the other ES checkouts under `~/Development/emulationstation-next.worktrees/` (the `m7-*` ones M7's, `qa-integration` another lane's, the `m6-*` ones the earlier slices') are read with `git -C ... show` only, never checked out or written; M7's October work on this file is cited by issue number
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, the session the dispatch comment on #682 names (`m6-t5-build-engine`; the brief's § 1: the T5 session, free since T33's close-out)
> **Epic:** #700 (the interface: T2 #649, T18 #665, T20 #667, T21 #668, T26 #673, T31 #678, T32 #679 and T33 #680 accepted, their issues open until the integration moves the pin on `next`; T34 #681 in flight or accepted as the dispatch comment says, its punch list #1307; this slice; T36 #683 and T37 #684 next, T44 after); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Independent -- **one seat, GPT-6 Astra at `max`** over a trimmed, scanned packet (D-WORKFLOW-195: **the 13 fork-added and fork-modified files whole** -- `LogPolicy.h` and the 12 -- 6,759 lines by the inventory's rule, **and of the 83 upstream-carried files only the ranges the questions cite**; nothing in the 96 is a binary; the expected scan hits are `SDL_Keycode`/`SDLK_*` names, the keyboard's key vocabulary, the four Ctrl debug toggles, the `maskSecrets` call sites (a function name beside the words it masks) and `LogPolicy.h`'s level tags, **every hit dispositioned by file:line in `packet-manifest.json`** as library plumbing, macro name, identifier or setting name, and a hit that is a value stops the packet; no value goes anywhere), a probe then one refutation; **exactly two keyed `tools/council/run invoke` calls**, every other council call with `COUNCIL_ENV_FILE=/nonexistent`.
> **The lens:** cost against value over the 96 paths of `es-core/**` as `rest` at the pin (22,575 lines by `grep -c ''`, 44 `.cpp`, 51 `.h` and `es-core/CMakeLists.txt`; the fork added one file, `LogPolicy.h`, and modified 12, +247/-71 over 19 commits with two merges; 83 byte-identical to ROCKNIX's master; 0 upstream commits on the 96 since the merge base `cada856d86` (14 on any path), so the merge debt is a one-line record, with batocera's twelve commits since `1750dded8c` on nine files, six of them fork-modified, as a reconciliation list for the integration, never a debt figure): the window and its floating surfaces, the input manager and its config file, the gun manager, the six es-core dialogs, the theme parser, the script runner, the watchers, the log; seven questions in the brief's § 4 (the window's queue and surfaces; the input's writes and the `<command>` execution; the watchers' lock; the lifetimes and #1305; `Scripting`'s quoting; the popups' accelerator, padding, help bar and words, with T34's inherited L-28 and L-29; cost against value, the structure and the merge debt), with the floor's pure leads 3.1 to 3.27 in the brief and the seven that FAIL at the pin plus 3.27's known FAIL first.
> **The rule:** **the lane changes nothing under the distribution's `packages/`, `projects/` or `tools/` at any stage, nothing in the ES worktree at stages A to D (it stays at the pin until stage E), and nothing outside the 96 paths at any stage**; `es-core/src/components/**` is T34's (#681), `resources/`, `utils/` and `renderers/` T36's (#683), `HttpReq.*`, `Settings.*`, `SystemConf.*` and `AtomicFileUtil.*` T21's (#668), es-app's files the earlier slices' (`CloudText.*` T18's, `GuiMenu.*` T26's, the other pages T31's with `GuiLoading.h`, the views and scrapers T32's, the game list, `SystemScreenSaver.cpp`, `NetworkThread.cpp` and `main.cpp` T33's, `SystemData.cpp` and `FileData.cpp` T2's) -- the globs decide; the three `tests/app-unit/fakes/` doubles of `Window.h`, `Log.h` and `LocaleES.h` are not the lane's to edit (a change to the signatures they double is named as a collision); T21's `3ae9610b0` hunk in `es-core/CMakeLists.txt` is the integration's; a fix in a neighbour is named for its owner at the pause; the nine earlier lanes' ES tips are diffed against the pin inside the 96 at stage A and at the hand-back, and every collision named; a defect is a `bug` with its trace, its `Already written:` line and its VM line (D-WORKFLOW-050, `bugs-are-agent-first.md`); a lead outside the 96 is a Backlog the coordinator files.
> **The host:** M6's and M7's by the shared log `/workspace/tmp/m7-m6-host-coordination.txt` (the durable successor of `/tmp/m7-m6-host-coordination-20261023.txt`, which the reboot of 2026-10-28 removed; M7 writes timestamped lines, not `== ` blocks: read the whole tail); this slice runs **one guest window with two boots**, asked for on #682 with its plan and bound after stage B and granted in the host file's queue: one GENERIC_X64 guest from M6's `069fc2704421` copy at `/workspace/artifacts/m6-t2-20261023/`, started at 640x480 (`generic-x64-vm run --headless --daemonize --res 640x480`; `vm-pair` has no option, #1141) and, for G-11, stopped by pidfile and started again at 1280x800 on the same disk; **30 minutes proposed plus 5 of grace** for a plan of 1,560 s (G-01 to G-12, the brief's § 5 item 2); the post contract `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` as each post's first line with the census (`qemu N, compilers N`), **the START post naming the detached timer that stops the guest at bound plus grace, or saying that nothing does** (#1135); the stop by pidfile at bound plus grace (`tools/vm-stop`, never a pattern), the disk retired after with path, size and sha (D-INFRA-022); the image identified by `BUILD_ID` and file name first and every frame labelled `image` or `pin-binary`; the card's two edges and a toast drawn after it, the keyboard's key gap at 640 and its size at 1280x800, the dialog's back landing on NO and on a last button, the empty row after CLEAR, the detect sentence in both languages, the screensaver over the transfer page, and G-01's `ldd` read for udev, each measured by a reader; the QA accounts only if a row needs one (none does, § 5; `tools/qa-accounts`, never printed; D-QA-016), never the owner's (D-QA-015)
> **Register:** the rows this brief cites are on the coordinator's branch, merged here; D-CLOUD-191 D-INFRA-031 D-LAUNCH-007 D-NET-017 D-QA-063 D-RA-052 D-SYS-013 D-UI-133 D-WORKFLOW-214 are the highest rows of their areas on the coordinator's branch (computed from the decided table at `be119338ff`; at `a00b3354d5` on 2026-10-31 the stranger's proof read D-CLOUD-191, D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052, D-SYS-013, D-UI-133, D-WORKFLOW-213), with the ownership row of the brief's § 1 written at dispatch (D-WORKFLOW-188 on the P1 branch only; the merge unites them); the four rows the brief's § 9 expects are put to the coordinator at the pause, never decided by the lane, and a row this slice forces takes an ID the coordinator assigns on #682
> **The brief:** `docs/reviews/briefs/es-core-window-input.md` at `8b5d9b9b62` (version 2 of 2026-10-31, after a stranger's proof of version 1 -- its corrections listed at its end, `## Corrections in version 2`); #682's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**Stage A done (2026-10-31); stage B next: `02` with its sections in § 6's order, then the window request on #682 with its plan and bound.**
- The audit folder is `docs/audits/2026_10_31-epic-m6-es-core-window-input/`: `00` (model, effort, `reviewed-at` `b1f2908a55` with the pin beside it, the host's tail and census at 06:00:08Z), `01` § Scope (the block's lines byte for byte, the § 5 figures), and `stage-a/` (first commands, membership, runs, host, issues).
- **Every figure is as the brief expects, with record-only deltas:** T34's ES ref resolves now (`dbe4c2db0f`, empty inside the 96); the block prints 30 claims (the prose's two `GuiLoading.h` rows are not in its `named` list); the lock grep prints six lines and `say(` three.
- The pointer's eleven keys read against § 10: none names T34. This worktree's six newer rule files were read.
- **Owed at stage B,** before `02`: § 3's line-cited reads (rules, register and `archaeology`, map, blindspots, tests, walks, French parser, audits, time to play), named in `01` as each is read.
- The ES worktree stays at the pin until stage E. Scratch is `/workspace/tmp/m6-t35/tmp`.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-core-window-input-682
cd "$D"   # no fetch of any kind: 651150fc88 and be119338ff are already in the repository
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git merge-base --is-ancestor be119338ff HEAD && echo coordinator-tip-merged
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                     # empty
git diff --stat b51dd8a805 HEAD -- packages projects tools | tail -1                  # empty; b51dd8a805 is b51dd8a805 at stage A
test -f docs/reviews/inventory.json && echo inventory
/usr/bin/grep -c -E '__[A-Z]+__|\b(CO''HASH|MERGE_''HASH|TIP''HASH|V2''HASH)\b' .github/sessions/saved-session-state-feature-m6-es-core-window-input-682.md   # 0: the brief's § 9 check; the quotes split each word so this line does not count itself (T34's seeded line had its hashes filled in and still counted itself, stage A)
W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-window-input-682
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l                      # the pin; 0
git -C "$W" merge-base 16dbac5211eea7e70db7394372033be2be7df829 rocknix/master | cut -c1-10   # cada856d86
date -u +%H:%M:%S; tail -n 6 /workspace/tmp/m7-m6-host-coordination.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
sed -n '1,150p' docs/reviews/briefs/es-core-window-input.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets, T5, T6, T7, T8, T23, T40, T11, T27, T25, T28, T9, T10, T12,
T13, T22, T14, T15, T45, T16, T29, T17, T18, T19, T20, T21, T33, T34, **then
this branch, with the pin moved to the ES branch's tip in the same
integration commit** (T21's `es-core/CMakeLists.txt` hunk and this slice's
reconciled there), then T36 and T37, then T4's last. When `next` moves, the
**coordinator** merges `next` into this branch, and never between stage A
and stage D; the coordinator merges its own branch into this one at
hand-back, before the last criterion's checkers run. Never merge another
lane's feature branch here, in either repository. Every lane and the M7
lane append to `docs/decision-register.md`, the day's work log and
`docs/work-logs/INDEX.md`: keep every append, regenerate the index, never
edit another lane's rows; a merge with conflicts is checked for leftover
markers before it is committed (#696), and a union of two ledgers is made
by whole entries. Nothing here builds an image, touches a device, a cloud
account, a provider, a key file, the host's swap, another lane's worktree,
or a guest outside the one granted window.

## Checkpoints

- stage A, 2026-10-31 06:03 UTC: distribution HEAD at the commit that carries this line (posted on #682), ES at the pin `16dbac5211` (clean); the block and the § 5 runs as the brief expects with record-only deltas
