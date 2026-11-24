---
name: build-cleanup
description: Free space on the build drive by removing pixelelated build leftovers. Keep at most one OS build (the one in progress, or the most recent while it is not yet on GitHub) and delete everything else a build or test generated. Use when the user says "clean up the build drive", "free up space", "remove old builds", "clean the leftovers", before and after every OS build, and whenever a cleanup pass holds or recovers nothing.
metadata:
  version: 0.1.0
---

# Build cleanup

Draft written by the one-on-one steward on 2026-11-24 at Max's request, integrated onto `next` by OS coordination (#493). It carries D-INFRA-035 and D-INFRA-036, which refine D-INFRA-033 and D-INFRA-034.

## The requirement, in Max's words

> The issue isn't whether or not we have enough space. It's that we want to proactively comply with my guidance that we only need to keep either the build currently in process or the most recent build (if it has yet to be uploaded to GitHub). Keeping all of these prior build artifacts takes up space we might need, and we can't predict when we'll need it. We want to remove leftovers and not just scrape by with enough space to do the next build. It's about maximizing the amount of available space so we can run concurrent builds, iterate, etc.

> If we need to change our script, if we need to change the process itself, that's fine, but we're fighting against ourselves.

> [The other project] is a totally separate project. [...] This should be treated completely independently of anything related to [it].

## Delete is the default

The goal is the most free space the drive can have. Room for the next build is not the goal and is never a reason to stop.

**What stays.** Only these:

1. **One OS build.** The build in progress. When none is running, the most recent build, which must stay while it is not yet on GitHub.
2. **Source.** Git objects and branches, and unique uncommitted edits saved as a patch.
3. **The shared download cache** that builds read, `/workspace/cache/rocknix-sources`.
4. **Compact records.** Receipts, logs, hashes and frames. These are kilobytes or megabytes.

**What goes.** Everything else a pixelelated build or test generated:

- `build.*` roots of every other build, on every target
- `target/` images and update tars of earlier builds
- per-checkout `sources/` copies and compiler caches of retired builds
- QA disks, extracted firmware and system images of finished tests
- scratch under `/workspace/tmp` and staging copies under `/workspace/artifacts`

A leftover is removed. Moving it somewhere else on the drive keeps the bytes and is not cleanup.

One specific item may stay outside the list above when someone names it with its size, the reason, its owner and the event that releases it. A class of things never stays.

## Done means

The inventory shows the keep set and nothing else, and `df -B1 /workspace` was read before and after. A pass that frees nothing while leftovers remain has failed and stays open. Passing tests, a timer that ran and "the next build fits" are not results.

## Procedure

1. **Measure.** `df -B1 /workspace`.
2. **Inventory, largest first.** List every generated directory with its size: the build worktrees (`tools/fork-worktree list`), nested `.build-runs/*/checkout` trees, `/workspace/tmp`, `/workspace/artifacts`.
3. **Name the keeper.** Is an OS build running? If not, which build is the most recent, and is it on GitHub? Everything else on the inventory is a leftover.
4. **Check pixelelated use only.** A leftover is in use when a pixelelated build, QA guest, build container or worker lane has it open:
   - a process with its working directory or an open file under it
   - a mount under it, or a running container with a mount under `/workspace`
   - a running build (`pgrep -f 'make docker-[A-Z]'`) or a QA guest's pidfile

   Other projects on the host are out of scope. Do not inspect, stop or wait on their services, and do not cite them as a reason to keep a pixelelated directory. Cleanup never needs a host outage.
5. **Save what is unique and small.** `git status --porcelain`, `git diff HEAD` as a patch, any untracked source file (`git ls-files --others --exclude-standard`), and confirm the branch still names the commit. Save nothing else.
6. **Remove.** A whole build worktree goes through `tools/fork-worktree remove <path> --force` after its listing. A generated directory inside a worktree that stays is removed directly. An empty directory, including a root-owned one Docker left as a mount target, is removed and never moved.
7. **Measure again** and write one receipt: the paths removed and the bytes before and after.
8. **Repeat** until the inventory is the keep set.

A destructive command may be stopped by the harness's own review. That is a real boundary. Ask Max once, in the lane that runs the command, saying exactly what is removed and what stays. Never work around it.

## When a pass holds

A hold is a defect in our tooling or process unless it names a live pixelelated consumer. Fix the script or the process in the same pass, or take the direct route in step 6. Do not report the hold as a result, and do not send Max a question he has already answered.

Each of these stopped the cleanup on November 23 and 24, 2026:

| What held | What it really was | What to do |
| --- | --- | --- |
| "The next build fits" | The wrong goal | Keep going until the inventory is the keep set |
| The tool refused checkouts at mode 775 as "shared" | Our own guard on our own directories; the group had no other members | Fix the guard or remove as the owner |
| The tool wanted an admission record | Paperwork the October builds predate | A build without a record is a leftover; apply the use check and remove |
| Item limits of 8,192 to 200,000 | Limits far below a real build of 870,000 to 3.6 million entries | A tool limit is a reason to fix the tool, never to keep the build |
| "Cannot prove no container on the host uses it" | A proof about another project's services | Check pixelelated use only |
| "Keep until a same-target successor" | A condition older than the one-build decision | Withdrawn by D-INFRA-033 |
| The batch failed moving an empty `sources/` to a keep directory | Preserving something that held nothing | Do not preserve leftovers |

## Why this skill exists

On November 23 and 24 a full sweep visited 53 checkouts and freed 0 bytes. 107 GB came back from caches while about 2 TB of old builds stayed. Max: "We've lost pretty much a day of work here." Every tool and rule involved kept by default and asked for proof before deleting. Each proof was one the old builds could not supply, and each hold was reported as progress. This skill reverses the default.

## Reporting to Max

Say which directories are gone, the free bytes before and after, and what is left that is not in the keep set, with the reason for each. Nothing else.

## Open question for Max

Once the most recent build is on GitHub it no longer has to stay. Whether to keep it anyway as a warm base for the next build is Max's call.
