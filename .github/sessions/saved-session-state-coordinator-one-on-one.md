# Saved session state — Max Coordinator one-on-one

## Start here

Resume **Max’s one-on-one steward** for the pixelelated project, an OS for handheld gaming devices. This is the direct conversation with Max. The steward owns the agenda, answers Max’s questions, relays his decisions once to the accountable owner, and verifies what came back. **OS work coordination** owns worker dispatch, build admission and host cleanup and maintains its [own checkpoint](saved-session-state-os-coordination.md). On every stash, archive the previous file for the lane being saved and update that lane’s file. The [shared index](saved-session-state-next.md) routes by role.

Saved **2026-11-24T03:31:17Z** in `pixelelated/distribution`, on `feature/conflict-resolution` in `/workspace/repos/rocknix.worktrees/conflict-resolution`. Canonical `next` is in `/workspace/repos/rocknix`. Check the incoming harness’s role and pane. Outgoing Codex was `w4:pF` (`01a209f0-f3e9-7991-885c-3847278f8b9f`). A harness switch starts a fresh native thread. OS coordination remains `w4:p2` (`01a0faa5-8103-73d3-8a42-456ab6c3b24b`). Keep these roles and their routing separate. Read `git show next:AGENTS.md` and the [lane guide](../../docs/lane-models-and-account-handoff.md). To read the saved agenda from either checkout, use `git show 06e00b25c6:docs/coordinator-one-on-one.md` and start at **November 24 harness handoff**.

## Current focus

Max asked why we kept failing to reclaim space on the 4 TB Serval build drive, asked us to record the failure as friction, and chose to switch harnesses. His retention decision is one OS build across all targets. Keep the in-flight build while building, otherwise the most recent completed build. A cold rebuild of an obsolete target is acceptable.

## Completed this session

- Recorded Max’s assessment, “We've lost pretty much a day of work here.” The steward reported passing tests, timer runs and enough space for staging while a production sweep visited 53 checkouts and freed zero bytes. We repeatedly sent a cleanup decision Max had already made back to him. The friction entry and shared operating rule assign follow-through on the largest actionable hold to the project. [Friction log](../../docs/friction-log.md) · [Storage issue #493](https://github.com/pixelelated/distribution/issues/493)
- Confirmed native eviction of 2,647,375 entries from 13 obsolete compiler caches. This batch returned **54,541,094,912 bytes**. All reported production batches together returned **106,887,766,016 bytes**. At 03:25 UTC, `df -B1 /workspace` showed **181,668,294,656 bytes available**. **Zero complete legacy build directories were removed.**
- Verified that the installed manual cleanup command keeps the whole-build backlog open after the actual zero-byte sweep. The separate full-profile implementation on local `next` (`e7e1a106a7`) passed its small opt-in tests. The October producers omitted the declaration it needs, and the old directories exceeded its limits. A passing test or enough space for the next build cannot close this backlog.

## In progress and open decision

The last verified keeper was the November 21 GENERIC_X64 Release05 build at `d7ca912480ea`. Two historical October SM8550 profiles originally occupied 166.55 GB, including caches already counted above. The build account and installed reader cannot verify every live container layer that might use those directories. **Serval stays online.** Max has already been asked whether OS may schedule one maintenance boot if live verification cannot clear the profiles. At this handoff he has neither authorized nor booked an outage. The switch of harnesses conveys no outage approval. Such a boot would interrupt Groundhog databases, SSH, Herdr and active agent sessions.

## Next steps

1. Check this one-on-one for any newer answer from Max. Retain the current online-only authority until he changes it. OS owns timing and execution of any authorized maintenance. The steward has no cleanup process to restart.
2. If Max asks for progress, read the original OS receipts and recheck `df -B1 /workspace`. Report newly removed production paths, measured bytes, and how many entire obsolete builds remain. If the evidence has not changed, use the existing hold and owner without rerunning the same scan.
3. Relay a new decision once to the verified OS coordinator, then follow the actual result back to Max. Routine worker traffic stays in OS coordination. Use the M7 milestone for project priorities and leave M6 assessment with its owner.

## Key files and related context

| Record | Use |
| --- | --- |
| `docs/friction-log.md` | November 24 at 03:27 UTC. Local `next` commit `20d8213a70`, working-branch commit `ef52788c69`. |
| `docs/coordinator-one-on-one.md` in the operating checkout | Direct conversation, decisions and history. Steward handoff `64272a441b`, incident history `06e00b25c6`. |
| `.claude/rules/worktrees.md` on `next` | D-INFRA-033 selects the keeper. D-INFRA-034 defines cleanup completion. |
| `docs/qa-logs/2026-11-23-build-directory-retirement/physical-bulk/20261124-sm04-reader-batches/current-slot/requested-cleanup/` in the operating checkout | `CACHE-RECOVERY.json` contains measured recovery, `PRODUCTION-PROFILE-COVERAGE.json` gives real build sizes and limits, and `MAINTENANCE.md` records the outstanding decision and service impact. These are local operating records on Serval. |

## Notes for the next session

Use the shared `session-resume` skill with this lane selected. The project has local work in both checkouts, and the operating worktree contains unrelated tracked and untracked changes belonging to other lanes. Preserve their work across the harness switch. The [M7 milestone](https://github.com/pixelelated/distribution/milestone/7) and [cleanup draft PR](https://github.com/pixelelated/distribution/pull/1440) carry project-level context.
