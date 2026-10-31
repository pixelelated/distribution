# Session pointer: M6.P2 T36, EmulationStation's utilities, resources and renderers: the file helpers and their cache, the process and shell helpers, the string and time helpers, the fonts, the texture cache and its loader, the GL renderers (#683)

> **Seeded:** 2026-10-31 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch (distribution):** `feature/m6-es-core-utils-resources-683`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch and `docs/reviews/{order.md,slices.json,inventory.json,status.md}`); the coordinator's tip merged in (`4bc59b6000` at `4b8285f4ab`, one merge, carrying the brief's versions 1 and 2 and its errata before dispatch, the futro's T36 kickoff addendum, the register rows the brief cites, the day's logs); the lane's own tip is `4b8285f4ab` (at stage A it is `4b8285f4ab`)
> **Worktree (distribution):** `/workspace/repos/pixelelated/distribution.worktrees/m6-es-core-utils-resources-683` -- the audit artifacts, the work log, this pointer and every ceremony live here
> **Worktree (EmulationStation):** `/home/max/Development/emulationstation-next.worktrees/m6-es-core-utils-resources-683`, branch `feature/m6-es-core-utils-resources-683`, cut by the coordinator from **the pin `16dbac5211eea7e70db7394372033be2be7df829`** (what `projects/ROCKNIX/packages/ui/emulationstation/package.mk`'s `PKG_VERSION` names at `8ebaf8daad`); the sources are read and the fixes are made here, on this branch only, and nothing is written here before stage E; **the pin bump in the distribution is the coordinator's**
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, no path of theirs named in a run, **no M7 build root read**; the other ES checkouts under `~/Development/emulationstation-next.worktrees/` (the `m7-*` ones M7's, `qa-integration` another lane's, the `m6-*` ones the earlier slices') are read with `git -C ... show` only, never checked out or written; M7's October work on this file is cited by issue number
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, the session the dispatch comment on #683 names (`m6-t1-os-launch`; the brief's § 1: the T1 session, free since T16's close-out)
> **Epic:** #700 (the interface: T2 #649, T18 #665, T20 #667, T21 #668, T26 #673, T31 #678, T32 #679, T33 #680 and T34 #681 accepted (T34's tip `49c6b43f27`), their issues open until the integration moves the pin on `next`; T35 #682 at stage E or accepted as the dispatch comment says, its tip read at stage A and never copied from here; this slice; T37 #684 next, T44 after); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Independent -- **one seat, GPT-6 Astra at `max`** over a trimmed, scanned packet (D-WORKFLOW-195: **the 15 fork-added and fork-modified files whole** -- the 6 and the 9 -- 6,212 lines by the inventory's rule, **and of the 43 upstream-carried files only the ranges the questions cite**, `utils/han.h` (20,923 lines) and `utils/zip_file.hpp` (10,011) never whole, a cited range at most; nothing in the 58 is a binary; the expected scan hits are `maskSecrets`' own vocabulary in `StringUtil.cpp:446-804` (the credential words it matches, its command names, the URL parameters it masks) and `OfflineProxyUrl.h:29`'s fixed header line, whose value is `1`, beside the loopback `Base` at `:22`, **every hit dispositioned by file:line in `packet-manifest.json`** as library plumbing, macro name, identifier or setting name, and a hit that is a value stops the packet; no value goes anywhere), a probe then one refutation (one in-call retry allowed); **exactly two keyed `tools/council/run invoke` calls**, every other council call with `COUNCIL_ENV_FILE=/nonexistent`.
> **The lens:** cost against value over the 58 paths of `es-core/src/{utils,resources,renderers}/**` less `utils/AtomicFileUtil.*` at the pin (50,840 lines by `grep -c ''`, 50,827 by `wc -l`; 25 `.cpp`, 32 `.h` and one `.hpp`; 14 under `renderers/`, 11 under `resources/`, 33 under `utils/`; the fork added six files and modified nine, `15 files changed, 1032 insertions(+), 60 deletions(-)` over 19 log lines with two merges, no `renderers/` file touched; 43 byte-identical to ROCKNIX's master; 0 upstream commits on the 58 since the merge base `cada856d86` (14 on any path), so the merge debt is a one-line record, with batocera's thirteen commits since `1750dded8c` on nine files, four of them fork-modified, as a reconciliation list for the integration, never a debt figure): the file helpers and their session cache, the process and shell helpers, the string helpers with `maskSecrets`, the time helpers, the launch command's word, the offline proxy's URL test, the zip reader, the math evaluator, the thread pool, the fonts with the fork's tab stops, the texture data, cache and loader, the resource manager and the seven GL renderer pairs; seven questions in the brief's § 4 (the file cache; the texture and font caches with #1263; paths and escaping; processes and the shell; the helpers' writes and false successes; the device reads, the renderers and the fork's text; cost against value, the structure and the merge debt), with the floor's pure leads 3.1 to 3.25 in the brief and the FAIL-at-pin candidates (3.1 to 3.10 and 3.14) first.
> **The rule:** **the lane changes nothing under the distribution's `packages/`, `projects/` or `tools/` at any stage, nothing in the ES worktree at stages A to D (it stays at the pin until stage E), and nothing outside the 58 paths at any stage**; `utils/AtomicFileUtil.*`, `HttpReq.*`, `Settings.*`, `SystemConf.*` and `es-app/src/ApiSystem.cpp` are T21's (#668), `es-core/src/components/**` T34's (#681), the rest of `es-core` (`Window.*`, `Log.*`, `ImageIO.*`, `InputManager.*`, `Scripting.*`, `es-core/CMakeLists.txt`) T35's (#682), es-app's files the earlier slices' (`CloudText.*` and `es-app/tests/unit/CMakeLists.txt` T18's, `GuiMenu.*` T26's, `SystemView.cpp` T32's, `FileData.cpp` T2's) -- the globs decide; `utils/DownloadFile.{cpp,h}` (T21's `3ae9610b0f` adds it under the glob; not at the pin, not among the 58) is a collision the hand-back names, never read, reviewed or fixed here; the `tests/app-unit/fakes/utils/FileSystemUtil.h` double is not the lane's to edit (a change to the four signatures it doubles is named as a collision); T20's `d9afa5c7c`, T21's `f7c16144d` and T26's S8 in `FileSystemUtil.cpp` and `Platform.cpp` are collisions read at stage A and never re-made; T35's case 3.11 is re-run unchanged from T35's tip, never edited (after T35's S6 it proves the caller's half only, and 3.13 alone tests the cache -- the errata); a fix in a neighbour is named for its owner at the pause; the ten earlier lanes' ES tips are diffed against the pin inside the 58 at stage A and at the hand-back, and every collision named; a defect is a `bug` with its trace, its `Already written:` line and its VM line (D-WORKFLOW-050, `bugs-are-agent-first.md`); a lead outside the 58 is a Backlog the coordinator files; no held directory is opened, and T34's held note for this slice is the coordinator's (ruling (k)).
> **The host:** M6's and M7's by the shared log `/workspace/tmp/m7-m6-host-coordination.txt` (the durable successor of `/tmp/m7-m6-host-coordination-20261023.txt`, which the reboot of 2026-10-28 removed; M7 writes timestamped lines, not `== ` blocks: read the whole tail); this slice runs **one guest window with two boots**, asked for on #683 with its plan and bound after stage B and granted in the host file's queue: one GENERIC_X64 guest from M6's `069fc2704421` copy at `/workspace/artifacts/m6-t2-20261023/`, started at 640x480 (`generic-x64-vm run --headless --daemonize --res 640x480`; `vm-pair` has no option, #1141) and, for G-06, stopped by pidfile and started again at 1280x800 on the same disk; **25 minutes proposed plus 5 of grace** for a plan of 1,080 s (G-01 to G-10, the brief's § 5 item 2); **an M6 window does not START while an M7 standing-functional START (#1293) is open on the host file -- it waits for that RETURN, which the slot's 300 s runtime bounds** (the coordinator's line of 15:43 UTC 2026-10-31); the post contract `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` as each post's first line with the census (`qemu N, compilers N`), **the START post naming the detached timer that stops the guest at bound plus grace, or saying that nothing does** (#1135); the stop by pidfile at bound plus grace (`tools/vm-stop`, never a pattern), the disk retired after with path, size and sha (D-INFRA-022); the image identified by `BUILD_ID` and file name first and every frame labelled `image` or `pin-binary`; the face, the theme and the libraries (G-01's `ldd` for `fribidi`, `vlc` and `freetype`), the font's scale at 640x480 and at 1280x800 measured by a reader beside `tools/font-stems`, the `exists` cache after a file another process wrote, the duration strings in English and French, the renderer through Mesa virgl with RSS before and after a scroll, and the pipe under the image's shell with the launch wrapper's copy, the running EmulationStation's `SigIgn` read first (the errata: the launch runs with SIGPIPE ignored, so the shell's 141 is not the launch's), each measured by a reader; G-08 and G-09 `CANNOT` as planned (the three renderers no image compiles; the handhelds' GL drivers); the QA accounts only if a row needs one (none does, § 5; `tools/qa-accounts`, never printed; D-QA-016), never the owner's (D-QA-015)
> **Register:** the rows this brief cites are on the coordinator's branch, merged here; D-CLOUD-193 D-INFRA-031 D-LAUNCH-007 D-NET-017 D-QA-063 D-RA-052 D-SYS-013 D-UI-137 D-WORKFLOW-216 are the highest rows of their areas on the coordinator's branch (computed from the decided table at `4bc59b6000`; at `acc4674006` on 2026-10-31 the brief read D-CLOUD-193, D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052, D-SYS-013, D-UI-133, D-WORKFLOW-215, and the kit's read at `ea8a4f52dd` printed D-UI-137 in D-UI-133's place, T35's stage-E rows D-UI-134 to D-UI-137), with this slice's ownership row of the brief's § 1, **D-WORKFLOW-216**, written at dispatch (D-WORKFLOW-188 on the P1 branch only; the merge unites them); the four rows the brief's § 9 expects are put to the coordinator at the pause, never decided by the lane, and a row this slice forces takes an ID the coordinator assigns on #683
> **The brief:** `docs/reviews/briefs/es-core-utils-resources.md` at `b1f34ce658` (version 2 of 2026-10-31, after a stranger's proof of version 1 -- its corrections listed under `## Corrections in version 2`, and what the proof left open under `## What version 2 does not settle`), **with its errata before dispatch at `e29a2966bc`** (`## Errata before dispatch`, eight items appended after the version line, version 2's text unchanged; where a section and that list differ, the list wins); #683's body carries its § 7 checkboxes, which the errata leave unchanged; where the two differ the body wins and the coordinator corrects the brief

## Current focus (16:42 UTC 2026-10-31 update): stage A done

**Stage A is done; stage B next (the audit folder is `docs/audits/2026_10_31-epic-m6-es-core-utils-resources/`).**

- **The pointer's eleven keys** were read against the brief's § 10 table: none names T35. § 9's placeholder grep over this file is `0`.
- **Done at stage A** (`00` and `01` § Scope; the scripts and outputs in `stage-a/`):
  - the first commands, with the ten lanes' ES tips (T35's `453dffd0a2`);
  - the membership block (its fourteen lines exactly as expected);
  - the 23 § 5 runs (every line as expected; the stage-C ones not run);
  - the angle includes under the lane's own list (33 non-standard of 241);
  - the three lanes' fixes read as collisions (T20 `d9afa5c7c`, T21 `f7c16144d`, T26 S8 `a5d2d3756`).
- **Stage B:**
  - `02` with its sections in § 6's order;
  - `ZipFile::extract` (`ZipFile.cpp:253-260`) and its caller read whole, and weighed under D-WORKFLOW-215's test before anything about them is posted;
  - the scoped `getCanonicalPath` lead (the dispatch's ruling (k) paragraph) read whole and weighed the same way;
  - then the window request on #683, with its plan and bound.
- **The ES worktree stays at the pin until stage E.** Scratch goes under `/workspace/tmp/m6-t36/`.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-core-utils-resources-683
cd "$D"   # no fetch of any kind: 651150fc88 and 4bc59b6000 are already in the repository
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git merge-base --is-ancestor 4bc59b6000 HEAD && echo coordinator-tip-merged
git diff --stat 8ebaf8daad HEAD -- packages projects | tail -1                     # empty
git diff --stat 4b8285f4ab HEAD -- packages projects tools | tail -1                  # empty; 4b8285f4ab is 4b8285f4ab at stage A
test -f docs/reviews/inventory.json && echo inventory
/usr/bin/grep -c -E '__[A-Z]+__|\b(CO''HASH|MERGE_''HASH|TIP''HASH|V2''HASH)\b' .github/sessions/saved-session-state-feature-m6-es-core-utils-resources-683.md   # 0: the brief's § 9 check; the quotes split each word so this line does not count itself (T34's seeded line had its hashes filled in and still counted itself, stage A)
W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-utils-resources-683
git -C "$W" rev-parse HEAD; git -C "$W" status --short | wc -l                      # the pin; 0
git -C "$W" merge-base 16dbac5211eea7e70db7394372033be2be7df829 rocknix/master | cut -c1-10   # cada856d86
date -u +%H:%M:%S; tail -n 6 /workspace/tmp/m7-m6-host-coordination.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
sed -n '1,150p' docs/reviews/briefs/es-core-utils-resources.md
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets, T5, T6, T7, T8, T23, T40, T11, T27, T25, T28, T9, T10, T12,
T13, T22, T14, T15, T45, T16, T29, T17, T18, T19, T20, T21, T33, T34, T35,
**then this branch, with the pin moved to the ES branch's tip in the same
integration commit** (T20's, T21's and T26's fixes in `FileSystemUtil.cpp`
and `Platform.cpp`, T21's `utils/DownloadFile.*` and this slice's
reconciled there), then T37, then T4's last. When `next` moves, the
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

- stage A, 16:42 UTC 2026-10-31: the distribution at the stage-A commit (named in the checkpoint on #683; `3740ce4a0d` before it), the ES worktree at the pin `16dbac5211`, unchanged
