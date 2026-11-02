# Session pointer: M6.P2 T41, the kernel patches and kernel configurations the shipped and test images apply, tabled by provenance and currency (#688)

> **Seeded:** 2026-11-02 by the coordinator (Opus 5.5 in the Antigravity CLI, lane `m6-coordinator`, D-WORKFLOW-189); the executor updates this file **at every checkpoint** (#1014)
> **Branch (distribution):** `feature/m6-patches-shipped-kernel-688`, cut from `feature/m6-renovation-plan-346` at `d7dd766659`, which carries `feature/m6-p1-survey-641` (`2174265e9c`) since `6a12ce2d73`; no merge commit; the lane's tip at stage A is this pointer's seed commit, the one commit over `d7dd766659` that adds this file (`git log -1 --format=%h` prints it; the dispatch comment names it) -- the brief's § 10 reads `d7dd766659` there, which the seed commit corrects (an erratum at acceptance)
> **Worktree (distribution):** `/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-kernel-688` -- the audit artifacts, the work log and this pointer live here; anything temporary under `/workspace/tmp/m6-t41/` after `df -i` (the tarballs' touched files under `/workspace/tmp/m6-t41/src/`), never `/tmp`, retired at stage H
> **Worktree (EmulationStation):** **none**: nothing in the 107 is EmulationStation's
> **Primary checkout:** `/workspace/repos/pixelelated/distribution` on `next` (D-INFRA-025); its object store is the coordinator's and every upstream read (`651150fc88`, `c445081a59`) goes there by `git -C ... show|diff|log|ls-tree <hash>`, never a fetch; the legacy `/workspace/repos/rocknix` and every `rocknix.worktrees/*` are the M7 lane's: read only, no process started there; the P1 research clone `/workspace/tmp/m6-coordinator/t11-research/tree` is § 2's block's `W`, read by `git -C` only
> **Repository:** `pixelelated/distribution`; every `gh` call carries `--repo pixelelated/distribution`
> **Executor:** Opus 5.5 at high effort, in the T3 session `m6-t3-emulators` (ruling (m)); record the model id your harness reports, never this line's label
> **Epic:** #1054 (`M6.P2 E339: Area epic: the patches and kernel configurations (T40, T41, T42, T43)`); T40 (#687) accepted at `e863379cec`, closed out at `bf3409ea18`, #687 still open; T42 (#689) and T43 (#690) after
> **Depth:** **Local -- a provenance table**: the executor alone; `review-plan.json` with reviewers `[]` and `tier_exception` D-WORKFLOW-184; no seat, no packet, no keyed call; the lint's Local proof at stage A
> **The lens:** package currency over the 107 of `patches-shipped-kernel` -- the kernel patches and configurations the shipped (H700, SM8550) and test (GENERIC_X64) images apply, 106 `.patch` and 1 `.conf`, 40,474 lines by the inventory and by `grep -c`, 40,473 by `wc -l`, five rows `non-kernel`; per row the target version, the pin, applies-at-pin, upstream status, backport status, the fork's reason
> **The rule:** **the lane edits none of the 107, no recipe, no tool, no script**; its commits touch only its audit folder, its retro, its pointer and its log entries; no `scripts/unpack`, `kconfig-*`, `adjust_kernel_config`, `check_kernel_config`, `kernel_make`, `config/options`; no fetch; no council, Facilitator or keyed call; a tarball extracted file by file into `/workspace/tmp/m6-t41/src/` only; a carried patch found wrong is a `bug` naming upstream's fix, never an edit (rulings (c), (g), (i))
> **The host:** **none**: no guest window and no compile; the host file `/workspace/tmp/m7-m6-host-coordination.txt` read once at stage A for its protocol and its line count (`1045` at dispatch); no START, RETURN or compile line of this lane's in it at any stage (ruling (h))
> **Register:** the highest decided row per area read from the table at `d7dd766659` (D-CLOUD-193, D-INFRA-031, D-LAUNCH-007, D-NET-017, D-QA-063, D-RA-052, D-SYS-013, D-UI-137, D-WORKFLOW-221), the last of them **this slice's ownership row, D-WORKFLOW-221, written by the coordinator at dispatch** (ruling (l); 220 is T39's)
> **The brief:** `docs/reviews/briefs/patches-shipped-kernel.md` at `9313492990` (version 2, sha256 prefix `24794608bcc7a0f9`, `2194` lines; version 1 `7d70da5972`, the stranger's proof `kit/t41-proof.md`)

## State at seeding

Dispatched 2026-11-02 05:26:00 UTC by the coordinator's comment on #688. Nothing has run. Stage A is next: the eleven keys above read against T40's and T39's values (any that names a predecessor is reported on #688 before going on), then the brief's § 5 `# STAGE A` block in order -- the lint's Local proof first (ruling (i)), § 2's block extracted from the brief at `9313492990` by its markers and never retyped (sha256 prefix `4d300124a6bf116f`), its 99 expected lines at P1 and at the tip, both line figures, the host file's protocol and line count, `00-running-log.md`'s header (the model your harness reports, the effort, the session, `reviewed-at` the tip with `2174265e9c` and `d7dd766659` beside it), `01-research-notes.md` § Scope, this pointer updated, and the day's work-log entry headed `#688`. **Every upstream command names `651150fc88`, never the ref `upstream/next`, which moves** (version 2, proof X01); stage A records the ref's value as information only.

## Next commands

```bash
D=/workspace/repos/pixelelated/distribution.worktrees/m6-patches-shipped-kernel-688
cd "$D"   # no fetch of any kind: every hash the brief names is already in the repository
git branch --show-current                                                            # feature/m6-patches-shipped-kernel-688
git merge-base --is-ancestor 2174265e9c HEAD && echo carries-p1
git merge-base --is-ancestor d7dd766659 HEAD && echo cut-from-the-coordinator
git rev-list --count d7dd766659..HEAD                                                # 1 at stage A: the seed commit
/usr/bin/grep -c -E '__[A-Z0-9_]+__' .github/sessions/saved-session-state-feature-m6-patches-shipped-kernel-688.md   # 0
git show 9313492990:docs/reviews/briefs/patches-shipped-kernel.md | sha256sum | cut -c1-16   # 24794608bcc7a0f9
date -u +%H:%M:%S; /usr/bin/grep -c '' /workspace/tmp/m7-m6-host-coordination.txt; tail -n 6 /workspace/tmp/m7-m6-host-coordination.txt | cut -c1-200   # the protocol and the line count only; this slice writes no line there
sed -n '1,120p' docs/reviews/briefs/patches-shipped-kernel.md                         # the opening, then § 1 and § 5 in full before the first STAGE A command
```

## Merge notes

The merge order is the coordinator's, named at acceptance. When `next` moves, the **coordinator** merges `next` into this branch, never between stage A and stage D; the coordinator's branch is merged into this one at hand-back, by the lane on the coordinator's word, before the last criterion's checkers run (T38's day-log conflict: keep both sides' entries in time order, regenerate the index). Never merge another lane's feature branch here. Every lane appends to `docs/decision-register.md`, the day's work log and `docs/work-logs/INDEX.md`: keep every append, regenerate the index, never edit another lane's rows. Nothing here builds, sources `config/options`, runs a guest, a council call or a skill against a provider, touches a device, a cloud account, a key file, the host's swap, another lane's worktree or an ES checkout, or edits any of the 107, a recipe, a tool, a rule, `CLAUDE.md`, `AGENTS.md` or `NAMING.md`.

## Checkpoints

- (none yet; the executor appends one line per stage: the stage, the tip, the time)
