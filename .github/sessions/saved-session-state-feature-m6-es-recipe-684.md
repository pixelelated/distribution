# Session pointer: M6.P2 T37, the EmulationStation recipe and themes in the distribution: the pin and its build steps, the build options and the renderer define, the dependencies, the build credentials by name, the shipped theme and `lowerdeck`, the patch directories, and package currency against ROCKNIX's recipe (#684)

> **Seeded:** 2026-11-01 by the coordinator (Fable 5.1, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch (distribution):** `feature/m6-es-recipe-684`, stacked on `feature/m6-p1-survey-641` at `2174265e9c` (which carries the P0 branch and `docs/reviews/{order.md,slices.json,inventory.json,status.md}`); the coordinator's tip merged in (`566398105e` at `94d8ef8e7e`, one merge, carrying the brief's versions 1 and 2, the futro's T37 kickoff addendum, the register rows the brief cites with this slice's ownership row, the day's logs); the lane's own dispatch tip is `94d8ef8e7e` (the merge; the coordinator's seeding commit `9fa740a91b` over it; filled at stage A from the dispatch comment and the coordinator's confirmation on #684, comment 6551486741)
> **Worktree (distribution):** `/workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684` -- the audit artifacts, the work log, this pointer, every ceremony and every fix (stage E, under `projects/ROCKNIX/packages/ui/` only) live here
> **Worktree (EmulationStation):** **none** (the brief's ruling (c)): the pin `16dbac5211eea7e70db7394372033be2be7df829` (what `projects/ROCKNIX/packages/ui/emulationstation/package.mk`'s `PKG_VERSION` names at `2174265e9c` and at `next`, blob `98cbc055d83f` at both) and every lane's ES branch are read by `git -C /home/max/Development/emulationstation-next.worktrees/qa-integration show 16dbac5211:<path>` (or `<hash>:<path>`) only; nothing is written in any ES checkout; **the pin bump in the distribution is the coordinator's, at the integration**
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there, no path of theirs named in a run, **no M7 build root read** -- so § 5's candidate-provenance read runs nothing there and cites R3 § 2.3 and cmd 21 (the brief's open item 16, answered by the dispatch comment); every ES checkout under `~/Development/emulationstation-next.worktrees/` (the `m7-*` ones M7's, `qa-integration` the one this slice reads the pin from, the `m6-*` ones the earlier slices') is read with `git -C ... show` only, never checked out or written; M7's October work on these files is cited by issue number
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, the session the dispatch comment on #684 names (`m6-t3-emulators`; the brief's § 1: the T3 session, `m6-t3-emulators`, free since T34's close-out)
> **Epic:** #700 (the interface: T2 #649, T18 #665, T20 #667, T21 #668, T26 #673, T31 #678, T32 #679 and T33 #680 accepted, their issues open until the integration moves the pin on `next`; T34 #681 complete; T35 #682 accepted at 00:24 UTC 2026-11-01 (`c9b2827eab`; the brief's § 1 and § 10, drafted before it, say handed back), its tips read at stage A and never copied from here; T36 #683 in flight, at the state the dispatch comment names, its tips read at stage A; this slice; T44 #691 after); the renovation epic #339; the milestone M6 (D-WORKFLOW-190)
> **Depth:** Independent -- **one seat, GPT-6 Astra at `max`** over a trimmed, scanned packet (D-WORKFLOW-195: **the 9 code files whole** -- the inventory's 327 read lines -- with **`emulationstation/package.mk:39`'s value masked** (the shared ScreenScraper identity's local), `es_savestates.cfg` (26) and `es_settings.cfg` (3) whole, **`es_features.cfg` (2,039) and `es_input.cfg` (1,810) by cited ranges only**, `Tiny5-OFL.txt` and the wordmark SVG named in the manifest and not sent, the four patches named for their owners and cited by range only where a question reaches them, the lane replacing these figures with the packet's own `wc -l` in the manifest; the expected scan hits are the ES recipe's five credential-name lines (`count lines: 5`: `:30`, `:40`, `:42`, `:43`, `:44`), **each dispositioned by file:line in `packet-manifest.json`** as *build-variable name* under D-INFRA-006, D-INFRA-007 and D-WORKFLOW-166, and a value that reaches the packet stops it; no value goes anywhere), a probe then one refutation (one in-call retry allowed); **exactly two keyed `tools/council/run invoke` calls**, every other council call with `COUNCIL_ENV_FILE=/nonexistent`.
> **The lens:** package currency over the 15 of `projects/ROCKNIX/packages/ui/**` -- the ES recipe `emulationstation/package.mk` (141 lines) with its `autostart/`, its four `.cfg` seeds, its three sources and its two units, `lowerdeck/package.mk`, and the theme's `package.mk` with `Tiny5-OFL.txt` and `pixelelated-wordmark.svg`; the four patches T40's (`emulationstation/patches/x86_64/cpugov.patch`) and T42's (the three theme patches) -- 4,561 lines by `grep -c ''` (the glob's 19 are 4,650 by `grep -c ''` and 4,649 by `wc -l`); fork-own 6, upstream-carried 9; 327 read lines in the 9 code files, 190 of them the fork-own files' (whose size is 572); the fork's change against the base `c445081a59` ` 8 files changed, 463 insertions(+), 13 deletions(-)` over 251 log lines with 5 merges, 246 non-merge, 241 of which touch the ES recipe; upstream's 16 commits on `ui/` since the base ` 8 files changed, 72 insertions(+), 75 deletions(-)`, and the tip to `upstream/next` `651150fc88` ` 14 files changed, 83 insertions(+), 536 deletions(-)`, `upstream-only 6 fork-only 6 both 2`; on the ES side the pin lacks 14 of `rocknix/master`'s (`f6c542872e`) commits and is 724 ahead, so the recipe's currency moves with the ES merge; seven questions in the brief's § 4 (the pin and its bump; the build options, the renderers and the install steps; the dependencies; the build credentials, by name; the themes and `lowerdeck`; the patches and their directories; package currency against upstream's recipe, the structure and the #585 lines), with the leads L-01 to L-21 in its § 3 and the FAIL-first candidates (L-02, L-03, L-07, L-08, L-04) first.
> **The rule:** **the lane changes only `projects/ROCKNIX/packages/ui/**` -- the 15 -- and only at stage E under a stream brief**; never `config/options` sourced in the worktree, and no `build.*` root there (every sourced-recipe call in the scratch export `/workspace/tmp/m6-t37/export/`, the brief's ruling (k); a `build.*` root in the worktree is a stop); never `PKG_VERSION` or `PKG_GIT_CLONE_BRANCH` of `emulationstation/package.mk` (the pin bump is the integration's, D-WORKFLOW-191 still open); never a pin or theme bump (a finding with its reason); nothing under `packages/` or `tools/`, nothing else under `projects/` (`virtual/image/package.mk` included, T8's); nothing in any ES checkout; `tools/pkgcheck <name>` by name after every `package.mk` edit, after its `find` positive, beside the control `es-theme-no-such-package`; the four patches' text is T40's and T42's, ES's top-level `CMakeLists.txt` the integration's, `es-core/CMakeLists.txt` T35's, the renderer bodies T36's, the dependencies' recipes T7's, T8's, T22's and T23's -- a fix in a neighbour is named for its owner at the pause; a defect is a `bug` with its trace, its `Already written:` line and its VM line (D-WORKFLOW-050, `bugs-are-agent-first.md`); a lead outside the 15 is a Backlog the coordinator files; no held directory is opened (`/workspace/tmp/m6-t34/held/` and `/workspace/tmp/m6-t36/held/` included).
> **The host:** M6's and M7's by the shared log `/workspace/tmp/m7-m6-host-coordination.txt` (M7 writes timestamped lines, not `== ` blocks: read the whole tail, with the time of the read); this slice runs **one guest window, one boot at 640x480**, asked for on #684 with its plan and bound after stage B and granted there and in the host file's queue: one GENERIC_X64 guest on a fresh disk made from M6's `069fc2704421` copy at `/workspace/artifacts/m6-t2-20261023/` in its own directory under `/workspace/tmp/m6-t37/` (`gunzip`, `qemu-img convert`, `resize` to 16G), never the `t2.qcow2` beside it, started with `generic-x64-vm run --headless --daemonize --res 640x480` (`vm-pair` has no option, #1141); **15 minutes proposed plus 5 of grace** for a plan of 780 s (G-01 to G-07, the brief's § 5 item 2); **no START while an M7 standing or compile START is open on the host file (#1293)**, the window queuing behind T36's slot; the post contract `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` as each post's first line with the census (`qemu N, compilers N`), **the START post naming the detached timer that stops the guest at bound plus grace, or saying that nothing does** (#1135); the stop by pidfile (`tools/vm-stop`, never a pattern), the disk retired after with path, size and sha (D-INFRA-022); the image identified by `BUILD_ID` and file name first and every row labelled `ui-equal` or `candidate`; every read through the device read filter, G-05's string counts as counts only; **the guest writes nothing** -- no file, setting or stamp, no reboot after first boot, no game, no cloud, no QA account; the owner's accounts never (D-QA-015); the guarded `tools/build-preflight --reclaim-swap` at most once, before the guest; the host-file compile lines (`T37 (#684) lane: stage <X> compiles START` / `END`) for every host compile, none while an M7 START is open -- and the brief allows no compiler; no build on the host at any time
> **Register:** the rows this brief cites are on the coordinator's branch, merged here; D-CLOUD-193, D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052, D-SYS-013, D-UI-137 and D-WORKFLOW-217 are the highest rows of their areas on the coordinator's branch (computed at stage A from the decided table at `566398105e`, `## Open decisions` excluded: `decided rows 699`; `tools/register-check` printed `713 IDs, each once`, `rc=0`; at `7d43f340c5` the brief read D-CLOUD-193, D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052, D-SYS-013, D-UI-137, D-WORKFLOW-216, and the kit's read at `926d1fbaee` printed the same nine), with this slice's ownership row of the brief's § 1 and § 9, **D-WORKFLOW-217**, written by the coordinator at dispatch (D-WORKFLOW-188 on the P1 branch only; the merge unites them); the rows the brief's § 9 says the pause may need (fribidi, the link, the patch directory, the freshness tool's reach, a loud catalog, the ARMSX2 block) are put to the coordinator there, never decided by the lane, and a row this slice forces takes an ID the coordinator assigns on #684
> **The brief:** `docs/reviews/briefs/es-recipe.md` at `926d1fbaee` (version 2 of 2026-11-01, after the stranger's proof of version 1 at `563857ea02` -- its sixteen corrections under `## Version 2: corrections from the proof`, and what neither version settles under `## Version 1: what the drafting read did not settle`); #684's body carries its § 7 checkboxes; where the two differ the body wins and the coordinator corrects the brief

## Current focus

**Stage C done (its checkpoint on #684); stage D next** -- the audit issue
as a sub-issue of #684 with the punch list, the bugs with their traces,
and the pause. Stage C's record: `tools/t37-checks.sh` (the tip exit 1,
`TOTAL: 55 of 60`; the fixed fixture exit 0, `66 of 66`; 15 of 15
mutations caught; the `.git` refusal exit 2), `03`, `04`, `05` (16 items:
4 Medium, 12 Low, each Open), the packet and its manifest (clean; `:39`
withheld by number), the probe and the refutation (exactly two keyed
invokes), the pre-issue lint. The window ran 01:42:09-01:44:35 UTC
(G-01 to G-07, the disk retired). Stage B's and stage A's records follow. Stage A's record: `docs/audits/2026_11_01-epic-m6-es-recipe/`
`00-running-log.md` (the model, the effort, `reviewed-at` `9fa740a91b`, the
host file read at 01:01:29-01:01:40 UTC, census `qemu 0, compilers 0`, the
export `/workspace/tmp/m6-t37/export/`), `01-research-notes.md` (§ Scope
with the block byte for byte, its sha256 `f3ef373be653546772d6f4be...`
checked in the file; every § 5 run against its expectation; open items 2,
3, 5, 9, 13, 15, 16 and 17, fribidi's path and L-22; the issues' states;
the lanes' tips; the register) and `stage-a/` (each script beside its
output). **Carry into stage B:** the mask `M` leaves `:39` unchanged, so
every recipe read withholds `:39` by line number too (the packet at stage C
included); T36's G-01 on the candidate image read `libfribidi` NOT linked
although ES's plan orders fribidi first (L-09's stage-B lead);
`tools/pixelelated-state-check` is not on the image (G-05's line, a
question with the window request); L-22's one image read is the
`noto-cjk` font path (a G-02 line, `candidate`); `HfsDBScraper.cpp:181` is
a fifth `HFS_DEV_LOGIN` reader. There is no ES worktree: the pin and the
lanes' ES branches are read by hash from `qa-integration`. Every sourced-recipe
call runs in the scratch export `/workspace/tmp/m6-t37/export/`, never
here, and a `build.*` root here is a stop. `.qa-scratch/` is gitignored and
`git status --short` is read before every `git add -A`; anything temporary
goes under `/workspace/tmp/m6-t37/`, never `/tmp`. No network is used
except the seat's two keyed invokes.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684
cd "$D"   # no fetch of any kind: 651150fc88 and 566398105e are already in the repository
git merge-base --is-ancestor 2174265e9c HEAD && echo stacked-on-P1
git merge-base --is-ancestor 566398105e HEAD && echo coordinator-tip-merged
git diff --stat 8ebaf8daad HEAD -- projects/ROCKNIX/packages/ui | tail -n 1         # empty
git diff --stat 94d8ef8e7e HEAD -- packages projects tools | tail -n 1               # empty before stage E; from stage E only projects/ROCKNIX/packages/ui/
ls -d build.* 2>/dev/null | wc -l                                                    # 0: a build.* root here is a stop (ruling (k))
test -f docs/reviews/inventory.json && echo inventory
/usr/bin/grep -c -E '__[A-Z]+__|\b(CO''HASH|MERGE_''HASH|TIP''HASH|V2''HASH)\b' .github/sessions/saved-session-state-feature-m6-es-recipe-684.md   # 0: the brief's § 9 check; the quotes split each word so this line does not count itself
Q=/home/max/Development/emulationstation-next.worktrees/qa-integration; PIN=16dbac5211eea7e70db7394372033be2be7df829
git -C "$Q" cat-file -e "$PIN^{commit}" && echo pin-here
git -C "$Q" merge-base "$PIN" rocknix/master                                          # cada856d86..., the whole line, no cut
date -u +%H:%M:%S; tail -n 6 /workspace/tmp/m7-m6-host-coordination.txt | cut -c1-200; pgrep -x qemu-system-x86 -r R,S,D,T | wc -l
sed -n '1,379p' docs/reviews/briefs/es-recipe.md                                     # the opening and § 1; § 2 opens at :380
```

## Merge notes

Merge order after the M7 candidate: `feature/m6-renovation-plan-346` (P0)
to `next`, then `feature/m6-p1-survey-641` (P1), then T1, T2, T3, T30, T24,
the packets, T5, T6, T7, T8, T23, T40, T11, T27, T25, T28, T9, T10, T12,
T13, T22, T14, T15, T45, T16, T29, T17, T18, T19, T20, T21, T33, T34, T35,
T36 (with the pin moved to the ES branches' tip), **then this branch, its
`emulationstation/package.mk` hunks merged over that pin-bump commit**
(the brief's § 8), then T4's last. When `next` moves, the **coordinator**
merges `next` into this branch, and never between stage A and stage D; the
coordinator merges its own branch into this one at hand-back, before the
last criterion's checkers run. Never merge another lane's feature branch
here, and never write in an ES checkout. Every lane and the M7 lane append
to `docs/decision-register.md`, the day's work log and
`docs/work-logs/INDEX.md`: keep every append, regenerate the index, never
edit another lane's rows; a merge with conflicts is checked for leftover
markers before it is committed (#696), and a union of two ledgers is made
by whole entries. Nothing here builds an image or a package, sources
`config/options`, touches a device, a cloud account, a provider, a key
file, the host's swap, another lane's worktree, an ES checkout, or a guest
outside the one granted window.

## Checkpoints

- **Stage A** -- `2ce981005e` over `9fa740a91b`, 01:20 UTC 2026-11-01 (accepted 01:21, 6551707733): `00`, `01`, `stage-a/`, this pointer's fills, the day's work-log entry; census `qemu 0, compilers 0`; worktree build roots `0`; keyed invokes `0`.
- **Stage B** -- the stage-B commit over `2ce981005e` (its hash in the #684 checkpoint post with the window request), 01:4x UTC 2026-11-01: `02`, `stage-b/`, `tools/t37-tables.py`, `00`'s stage-B entries; census `qemu 0, compilers 0`; worktree build roots `0`; keyed invokes `0`; no guest.
