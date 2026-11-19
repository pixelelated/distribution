---
name: herdr-project-coordination
description: Coordinate parallel projects through visible Herdr lanes, project managers, scoped assignments, and dependency handoffs. Use when the user requests Herdr-based multi-agent project coordination or asks to keep those lanes progressing. Does not authorize delegation, new projects, or external actions by itself.
---

# Herdr project coordination

Use a small hierarchy: the portfolio coordinator owns priorities and shared decisions; each project manager owns that project's plan and integration; workers own bounded deliverables. Keep the work visible in Herdr. Internal subagents can assist, but do not describe them as Herdr lanes.

This is an experimental operating practice. Improve it from observed coordination failures; do not add process merely to keep agents occupied.

## Project lane models and native login

For pixelelated OS and codebase renovation, use the current `next` version of
`tools/herdr-lane fresh` or `resume` and `docs/lane-models-and-account-handoff.md`.
Pin Codex coordinators to `gpt-6.2-astra` and workers to `gpt-6.2-sol`, both
at `xhigh` with approved sandbox and review. Preserve Claude seat tier using
`claude-fable-5-2` or `claude-opus-5-5` and its native permission settings.
On a user-initiated switch, identify shared stores, authenticate once per native
harness/store, retain the pinned thread and worktree, and read back effective
model, effort and review before dispatch. The designated rollout owner handles
live sessions. Reconcile incomplete work from original results.

## Establish the visible topology

1. Verify `HERDR_ENV=1` before any Herdr inspection or control. If absent, explain the limitation and stop Herdr actions.
2. Read the installed `herdr --skill` unless already in context. Use its current CLI help and safety rules rather than copying an old command recipe. Use explicit returned pane IDs or unique agent names, preserve user focus, and inspect startup/approval failures before further input.
3. Inspect existing workspaces and agents. Reuse the relevant project lane; do not duplicate managers or interrupt unrelated work. Create topology only within the user's requested arrangement. Separate projects should use their assigned worktrees; same-project workers may share a tree only with explicit disjoint write ownership.
4. Map each active project to a visible workspace/pane, live agent name, worktree, and accountable manager. A sidebar workspace without a working agent is not an active lane. After prompting, verify observed work or an acknowledgment; successful submission alone proves only delivery.
5. Show the user the new lane names and their current task. If an internal manager is coordinating existing visible workers, say so. Do not imply the manager itself has a Herdr pane.

## Separate human conversation when requested

When the user asks to separate direct conversation from worker coordination,
create or reuse the requested human-facing lane and keep operational traffic in
the work coordinator lane. Preserve one accountable worker dispatcher; a
one-on-one steward owns conversation, priorities/questions and action-item
follow-up, not a second worker queue. Record exact lane/session identities and
disjoint write ownership in the project's existing continuity entrypoint.

Keep the human lane slower-moving: concise material outcomes, actionable changed
blockers, open questions and meaningful follow-ups. Do not forward raw worker
transcripts, routine ACKs or unchanged monitor ticks. Link one compact agenda to
the canonical priorities and evidence; give each item an owner, next event/action
and disposition. User decisions retain their exact scope and durable reference,
are relayed once to the dispatcher, and remain pending until consumption is
observed. Inspect ambiguous delivery before retrying. Existing authorized work
continues without passing through another human approval relay.

Preserve existing worker/monitor destinations when renaming the operational
lane; do not subscribe the one-on-one pane to worker-reminder traffic. Verify
agent readiness and handoff acknowledgment before calling the new lane active.
If startup is blocked, report the actual blocker and finish independent routing
and instruction work without answering an approval UI. At the next real user
decision/worker return, check whether the split reduced noise without losing
follow-through or duplicating dispatch; use the existing retrospective loop.

## Treat human-pane prompts as human-visible messages

A prompt to the one-on-one steward appears in the user's conversation. It is not
private agent transport. Write it for the user before delivery: a meaningful
outcome, new or materially changed blocker, or understandable required decision.
Answer actual user-requested status. Keep ACKs, receipt requests, internal event
IDs, unchanged pending-approval checks and routine report deadlines in operational
evidence. A promised checkpoint alone does not justify another unchanged message.

Use the project's existing filtered delivery mechanism; do not bypass it with
ad-hoc human-pane prompts. The steward reads shared result artifacts and actual
activity for verification. Do not send an internal completion or receipt prompt
back to the human lane. Preserve separate delivery/consumption/publication states
locally and never infer human reading. Keep genuine new stoppages visible even
when a solution is unfinished; state ownership without inventing a user question.
Filtering known operational text cannot prove semantic novelty: the coordinator
and steward must also judge whether the message changes anything for the user.

## Escalate stopped work to the human channel

When a planned step stops on a blocker, proactively notify the designated human
conversation lane. State what stopped, when observed, cause/impact, accountable
owner, the concrete action needed and the next update. If a request is not ready,
keep preparation owned and visible; do not silently wait on the user with an
expired or unfinished proposal. Continue independent authorized work.

Use the existing scheduler and escalation mechanism when available. Track human
notice intent/submission, steward consumption, user-facing publication and blocker
resolution independently of routine monitor ACKs. Preserve unresolved state on
continuation and deduplicate unchanged incidents. Verify the pinned target before
sending. Ambiguous delivery needs reconciliation, not blind resend; report
unavailable delivery and do not imply the human read a published notice. A
one-on-one steward is not another worker dispatcher or approval gate.

Verify controlled stopped-work, failure and ACK-independence cases and a real
blocked transition. Check detection-to-actionable-publication and missed updates
in the existing retrospective loop; prose alone does not implement escalation.

## Keep one compact coordination record

Use the project's existing task or planning system when available. Otherwise keep one small local ledger outside unrelated source changes. Track:

- Project/issue and acceptance boundary.
- Manager, Herdr lane, worktree, current owner, and authorized write scope.
- Current deliverable, dependency/blocker, next useful task, and update time.
- Evidence/result location and verification level: proposed, source reviewed, tested, integrated, or actually exercised.
- Shared resource ownership or explicit runtime hold, when relevant.

An external issue tracker records scope and durable progress; Herdr shows live execution. Keep their meanings distinct. Historical results stay attributed to the version tested. Do not rewrite old records to make them appear current.

## Assign work that can converge

Before dispatch, read the complete issue/criteria and the available handoff. Revalidate saved next steps against scope. Inventory existing seams once, then turn findings into a concrete change, review, decision, or experiment. Do not serially rename the same inventory as new work.

A useful assignment states the desired result, exact ownership, relevant inputs, meaningful verification, dependency boundary, and return destination. Include explicit exclusions only where they prevent a likely conflict. Reuse completed evidence rather than sending every worker through the entire history.

Use a project manager when a project has multiple dependent lanes or needs sustained sequencing. Do not spawn another hierarchy for a single small task. Before handing management to a new agent, transfer the current plan and close the previous manager's dispatch authority for that project; two managers must not independently assign the same workers.

Project managers may continue already authorized next steps without repeatedly asking permission. A returned result is not new authority for unrelated work, commits, deployment, private data, or costly runtime. Respect explicit source-only or one-use runtime scopes. Escalate a concrete decision with its prepared evidence, not an unfinished proposal asking whether to begin.

Keep authorization separate from readiness. Routine private preparation and coordinator-owned selection/admission/START records within the agreed scope do not require another human yes. Verify actual prerequisites and preserve one-use, resource and expiry limits. On an explicit approval, reconcile stale approval blockers in the existing ledger and observe the next owner start. Escalate a genuine scope/effect change, unresolved consequential choice or actual enforcement rejection; do not bypass platform controls or mistake a repository policy edit for a platform settings change. Once the required decision resolves a rejection's condition, continue the authorized step without asking the same question again.

## Discover portable standing authority

Use the project's canonical repository instructions before interpreting worker
limits as coordinator-wide restrictions. For pixelelated, D-WORKFLOW-196 in
`docs/build-authority.md` and `.claude/rules/device-builds.md` authorizes routine
host preparation/assembly, builds and isolated tests, including internal
activation/START and workload execution under current admission and platform
review. Both AGENTS.md and CLAUDE.md on canonical next discover it; an installed
skill is supplementary. Cite the authority and actual effects directly when
requesting platform review. Preserve original rejections/spent attempts and use
only supported evidence/review routes, never a workaround. Operation-specific
caps differ; a short assembly budget is not a universal OS-build limit. Reconcile
current live plans/owners; standing permission does not reactivate old tasks.

## Keep parallel and serial work separate

- Parallelize independent source changes, product decisions, tests, and reviews where file and resource ownership allow it. Reserve shared source integration, schema changes, and bounded runtime to one named owner.
- Prepare dependent work against an immutable candidate when useful; identify its dependency and avoid reading a producer's moving files as a reviewed result.
- On completion, reconcile the result with acceptance criteria, integrate or release the next authorized step, and update the lane's next task. If blocked, name the exact missing input and owner.
- Move a blocked worker to a useful independent task within authorized scope when one exists. Otherwise mark the lane ready/blocked honestly; inactivity can be correct. Never manufacture reviews, unnecessary tests, or new scope to keep status “working.”
- Internal agents and external Herdr agents have different capacity limits. Respect both and avoid scheduling heavy suites, databases, or browsers concurrently just because another agent slot is free.

## Keep useful backlog work moving around a blocked branch

A real approval or resource block applies to its dependent branch. Read the
current ordered plan and open criteria beyond already-completed assignments.
Resolve coordinator-owned prerequisites; while a genuine decision is pending,
select the highest useful independent authorized task. Record each skipped
candidate's specific dependency and owner, then examine the next. Completed lane
tasks do not prove an empty ready backlog. Preserve project boundaries and do not
mistake an active priority label for an actually working owner.

Before dispatch, retain full issue criteria, priority evidence and disjoint write
ownership. Reuse a verified available lane, observe actual start, consume its
useful return and continue the next supported action. Do not manufacture reviews,
replay accepted tests or renew a rejected operation's budget to fill lanes. Keep
selection/start/result evidence in the existing ledger and check the next real
blocked-branch cycle; do not add a competing queue or serial approval framework.
Keep operational details out of the human lane under its existing delivery rules.

## Verify the actual execution and reporting route

After login or UI recovery, reconcile pinned processes, retained effects and
pending returns before continuing; a settled authentication failure is not a
completed task. Check live writable roots against owned output/report paths.
Use supported narrow launcher permissions or a suitable already-writable owner;
a config/schema option is not proof it changed the running managed session.
Preserve platform review and never answer another lane's approval UI.

Preflight the actual prepare/run/save/retire path, including the same report
writer and representative payload size, before expensive work. Preserve full
originals once, then use compact immutable references/current state through
existing tooling. Derive fresh workload and reporting budgets from observed
costs plus cleanup reserve; never extend spent attempts. Continue useful results
and independent backlog with observed starts or specific dependency owners.
For pixelelated these five changes are D-WORKFLOW-197 in `docs/build-authority.md`;
use that portable contract, not this installed skill as sole authority.

## Use proportionate checkpoints

Choose checkpoints around useful milestones and uncertainty. For normal source work, ask for an early blocker or substantive update and a final result; avoid tiny entry windows and repeated approval relays. Use strict expiry and resource budgets when the actual action requires them, such as a one-use runtime lease.

Record actual start and elapsed time honestly. A missed checkpoint is a coordination issue to report and adjust prospectively, not permission to backdate or silently extend a hard stop. If a unit has a hard stop, preserve useful partial work and return it. Ordinary progress estimates are not automatic cancellation policies.

Managers monitor their own workers and report changes in outcome, dependency, or risk to the portfolio coordinator. Use event-driven messages where possible. Do not repeatedly prompt an agent that is working or blocked. A stalled prompt or timeout requires inspection before resubmission.

## Close the loop visibly

Report outcomes in product terms, then the evidence and remaining limit. Distinguish “tests passed” from “source appears correct,” and recorded cleanup from verified current resources. Do not bury users in hashes when a short linked result suffices. Use stronger immutable evidence only where the task's risk or concurrent custody needs it.

At a project transition, leave a compact handoff: what changed, what was verified, unresolved decisions, next owner/action, and resources still held. Keep long-lived lanes available unless the user asks to close them. Never close or rename unrelated panes.

Periodically assess whether the hierarchy improves time to a reviewed deliverable: duplicated work, blocked time, handoff cost, escaped ownership conflicts, and user visibility. Simplify the process when coordination costs outweigh useful parallel progress.

## Close the progress loop, not just the notification loop

A completed worker notification creates a coordinator obligation. In the same active turn, read the new result once, record its disposition, and either start the next authorized task with observed working evidence or name the dependency owner and next check. A saved checkpoint, successful prompt submission, or `complete` acknowledgment alone does not prove that the next task started. Do not wait for the user to nudge already authorized work.

Keep these states distinct in the existing ledger: returned/unconsumed, selected/not started, working with an observed start, blocked with an exact dependency and owner, and intentionally idle with no useful authorized work. Each nonterminal handoff needs a next-check time or named dependency event. A blocker on one lane does not pause independent lanes. Do not invent busywork, widen scope, or repeatedly review accepted artifacts to fill idle time.

An acknowledgment resolves the returned-event notification only. Keep its linked successor/dependency obligation independently until observed start or an explicit revised/closed disposition; acknowledging a return must not erase selected-but-unstarted monitoring.

When background monitoring is requested, prefer the existing scheduler and lock. Monitor three things: worker events, coordinator consumption/start evidence, and the monitor's own health/lifetime. A timer that reports worker completion but silently expires, or treats prompt submission as acknowledgment, is incomplete. Keep a finite notification budget and cooldown; reconcile saved delivery state and current session before an overdue reminder. An ambiguous prompt response is not permission to replay a task. Reminders carry event identity and reconciliation instructions, never duplicate workload commands. Never answer an approval UI, bypass a usage limit, or assume a missing agent can be restarted.

Name who owns observer renewal before it expires and what exposes an unavailable coordinator or exhausted reminder budget. If no independent off-session delivery destination exists, say so; a local alert is not delivered to the user. A usage reset resumes by reading pending returns and running owners first, not by rebuilding queues. Preserve expiry and resource constraints on workloads; renewing an observer grants no execution authority.

At each useful coordinator checkpoint, inspect overdue unconsumed and selected-not-started items, then continue runnable work. Before yielding, record which lanes are working, what the others await, the next expected event/check, and the actual observer health/expiry. Keep product updates concise. Do not describe every lane as active merely because its tab exists.

Use the existing retrospective/work-log loop to measure recurring stalls: completion-to-consumption, selection-to-observed-start, observer gaps, and duplicate notifications/dispatches. Treat unknown times as unknown. Compare the next real handoff against the change; a passed unit test or one successful cycle is not sustained effectiveness. For each recurring cause, distinguish an absent rule, a rule that was not discovered, and a known rule bypassed under load. Improve guidance, discovery, or the execution boundary accordingly; stronger reminders alone do not fix the third case. Retain the cause, alternatives, chosen change and next real outcome that could disprove it in the existing work log. Repeated notices for one return are not independent incidents. Review the remedy itself for added serial work: consolidate already-authorized handoffs that protect no distinct boundary, and remove redundant controls rather than accumulating review gates.

## Preserve the work obligation across checks

For recurring unchanged checks, retain the work/dependency identity, original
no-progress age and finite reminder budget. A new tracking record, ACK, check
timestamp, agent activity or repeated evidence is not a new prerequisite outcome.
Distinguish coordinator-owned preparation still to do from an actual external
wait. In the same active turn as a completion or approval, perform the next
necessary authorized action or produce a concrete supported blocker; notification
bookkeeping alone is not continuation.

Where supported, feed completion events into the existing observer and durable
ledger; reconnect with an identity-checked snapshot and keep scheduled health
checks as recovery. Do not add another dispatcher or worker queue, and suppress
agent wakeups for unchanged intentionally idle state. Validate event/reconnect
behavior and the next real completion-to-action cycle separately.

Do not infer that the coordinator needs a new human yes from a worker's
source-only assignment or an empty internal permission/admission field. Identify
the governing user scope or actual enforcement refusal. Finish root-owned
readiness before starting finite input lifetimes; keep platform review and
one-use constraints intact. If a prepared route cannot satisfy an actual context
predicate, fix that precise source/selection problem rather than renewing a hold
while work remains unready.

## Preserve continuity across agents and harnesses

Use the repository's continuity/handoff conventions when available. Keep one
discoverable current entrypoint linking scope, worklog, decisions, recurring
friction, current owner and next useful task. A new agent should not need the
previous conversation to orient. Put local friction episodes in the worklog and
promote recurring lessons to the existing project register, not another tracker.

At material milestones and before a planned session/provider switch, preserve
uncommitted candidates and evidence in the appropriate durable location. Do not
rely on `/tmp`, ignored notes, a branch name or harness memory as a backup. Keep
sensitive provenance in approved owner-controlled storage outside Git. State
whether artifacts are local, committed, published and backed up; these are
different guarantees. Repository guidance must remain usable without this skill.

Before transferring management, stop new dispatch for that scope and record the
receiving owner, exact changes, verification limits, pending decisions, authority
expiry/consumption, active effects and cleanup obligations. Retain or explicitly
transfer monitoring duties. Credit exhaustion or session loss does not cancel a
process or establish return. After an unexpected stop, reconcile uncertain effects
under existing authority before retrying; never renew a lease from a saved note.
Checkpoint during useful work because a final warning may never arrive.

For a substantial handoff, have the successor locate the next task and limits
from the saved entrypoint, and verify the selected artifacts without executing
them. Record missing closure and off-device recovery gaps honestly.

## Understandable decisions and effective escalation

A human question must stand on its own: the product outcome, proposed
practical action, meaningful choice, consequence/tradeoff, recommendation and
specific reason existing coordinator authority cannot settle it. Link technical
proof; do not make the user interpret worker names, file counts or hashes.

First distinguish routine technical arrangements from a governing user limit or
actual platform refusal. Quote that boundary accurately, including its scope.
Worker assignment exclusions, internal null fields and coordinator-authored
proposals do not establish a human gate. If no consequential human choice is
established, keep preparation with the coordinator and continue authorized work.
A withdrawn or unintelligible question is not an external wait or tacit approval.
Preserve real limits; do not route around a refusal or renew a spent commitment.

When an outcome stops, promptly say what stopped, its impact, observation time,
owner, whether a user action is actually ready, and the next update—even while
preparing a solution. Sent/consumed receipts establish transport events, not
understanding or effective escalation. Preserve late updates and unresolved
state; never use receipt bookkeeping to dismiss the user's report of poor
visibility. Apply this through the existing handoff and retrospective process.


## Verify recurrence corrections against the failed handoff

For root-owned preparation, do not end a turn with only an ACK and a later
checkpoint. The existing monitor must retain the obligation and refuse unchanged
postponement; stale working/preparation needs the same human visibility as an
explicit blocker. Neither agent activity nor a renamed evidence file proves an
outcome. A genuinely new prerequisite result can advance the record; a real
external wait names the exact action and accountable owner. Preserve actual
refusals without inventing approval gates from internal fields.

A recurring-stall retro compares the previous remedy with the retained failed
turn. Verify the control against that case, distinguish source/test/deployment
from real next-action evidence, and review counterexamples at the next handoff
and weekly summary. Do not make the retro another gate or claim that policy text
or one successful run guarantees prevention.


A genuine prerequisite result can still leave the next preparation step dormant
when the coordinator ends its turn. Reconcile the pinned root's settled state
against unfinished owned preparation immediately, even with a future report
checkpoint. Use the same observer, lock and obligation identity; completion
sequences and reconnects do not replenish unchanged work's finite wakeup budget.
Let the first genuine handoff bypass unrelated notice cooldowns, suppress it for
intentional idle or an evidenced external wait, and expose exhausted continuation
through the existing human escalation. Never prompt through a blocked UI or
adopt a changed session. Verify event-to-delivery in isolation, then the next
natural turn-end-to-action separately; neither notices nor synthetic tests prove
sustained progress.
