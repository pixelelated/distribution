---
description: "Which ceremony is owed and when -- a friction entry's issue, a mini-retro, the weekly and monthly summaries, the work-log index, the register lint, a blindspot's guard, a code audit, a futro -- as a state machine tools/ceremony-check reads from the record; what a missing one refuses (D-WORKFLOW-028, D-QA-040)."
---

# The ceremonies are a state machine, and a tool turns it

*No `paths:` glob, so this file loads every session: a ceremony is owed by the
calendar and the record, not by the file being edited.*

The skills that look back and forward -- `mini-retro`, `futro`,
`begin-delivery`, `code-auditor`, `council` -- ran at phase boundaries
through 2026-09-14 and not once in the nine days of release-candidate cuts
that followed, during which blindspots 47-52 were written. A ceremony tied
to a boundary never fires when the work has none. So the cadence is read
from the record by `tools/ceremony-check`, refused by the push guard when a
cheap artifact is missing, and kept red in the fork's CI while a long one is
owed (D-WORKFLOW-028; the numbers are D-QA-040, the maintainer's call).

Maintainer, 2026-09-23: *"Do we need to build this into our CI workflow
itself so that we're running some of these processes as state machines that
are mandatory, as opposed to things that are just optional?"* Yes.

## The states, their markers, and what each one costs when missed

| Ceremony | Marker the tool reads | Cadence (D-QA-040) | When overdue |
| --- | --- | --- | --- |
| Friction entry | a line in `docs/friction-log.md` with `issue: #N` or `guard` | an issue or a guard within 3 days of the line | **refuses a push of next** |
| Mini-retro (phase tier) | `docs/retros/<date>-<scope>.md`, or a work-log heading that says retro | every 5 active days, grace 2 | refuses a push |
| Weekly summary | `docs/work-logs/<yyyy_mm>-work_logs/<yyyy>-W<ww>-summary.md` | by the Tuesday after the week | refuses a push |
| Monthly summary | `docs/work-logs/<yyyy_mm>-work_logs/SUMMARY.md` | by the 3rd of the next month | refuses a push |
| Work-log index | `tools/work-log-index --check` | with every log entry | refuses a push |
| Register lint | `tools/register-check` | always | refuses a push |
| Test drives | `tools/test-drive-check`: a fork commit on `next` after the tool's adoption that touches a product path in `docs/qa/test-drives.txt` changes its test, or carries a `Test-drive:` or `vm-qa: <BUILD_ID> PASS` trailer (D-QA-066, #1468) | every new fork commit, including merges | refuses a push |
| Issue ownership citation | fork commits on `next` after `bf121ce876` cite `#N` in the message or in `docs/issue-citations.txt` (#1444); upstream and pre-adoption history excluded (D-WORKFLOW-132) | every new fork commit, including merges | refuses a push |
| Blindspot guard | an entry from 52 on names a `tools/…`, `.githooks/…` or `.claude/rules/…` that exists | with the entry | refuses a push |
| Code audit (epic/milestone tier) | an issue titled `Audit:` / `Code audit`, or `docs/audits/<date>-*/` | after 12 completed closures or 14 days | **CI red**, the push goes through |
| Futro | `docs/futros/<date>-<scope>.md`, or a work-log heading that says futro | within 3 days of a new `epic` issue | CI red |
| Open checkboxes agent-verifiable | `tools/box-check`: no open `- [ ]` names a person or a device without a physical fact (D-QA-044) | always | CI red -- the fix is a tracker edit, as with issue hygiene |

The split is deliberate: a friction line, a retro, a summary and an index are
minutes, so a missing one stops the push until it is written; an audit is
hours, so it stops the badge, not the fix that is in hand. If a cheap gate is
ever bypassed with `--no-verify`, that is the friction entry to write.

The clock starts 2026-09-21. Nothing before it is demanded; a backlog nobody
can pay at once is how a gate gets switched off.

The completed-audit marker is `docs/audits/<scope>/audit-completion.json`.
After Phase 7, retain exact closed/completed tracker readback and its verified
timestamp, hash-bind the analysis, punch list and tracker receipts, and run
`tools/ceremony-check` without `--gate`. A phase-prefixed issue title or an
underscore-dated folder does not reset the legacy start-date heuristic; the
existing completion-marker validator and resolution lint must accept the actual
finished audit (#540). Do not rename historical evidence or repeat a completed
external review to repair missing bookkeeping.

## The timescales (Pongogo's layers, adapted)

- **The day**: `docs/work-logs/<yyyy_mm>-work_logs/<yyyy_mm_dd>-work_log.md`,
  a timestamped entry per thing learned or decided, appended as it happens
  (`learning-capture.md`). The heading names the issue and the thing, since
  `tools/archaeology` finds entries by their words.
- **The index**: `tools/work-log-index --write` after an entry;
  `docs/work-logs/INDEX.md` lists every entry under its day, ISO week and
  month, so a month reads in a minute.
- **The week**: the retro writes `<yyyy>-W<ww>-summary.md` beside the day
  files -- what landed, what was hard, what changed in the rules, the
  blindspots added, the issues opened and closed -- from the index and the
  friction log, not from memory.
- **The month**: `SUMMARY.md` in the month's directory, from the weeklies:
  the arc, the decisions (by ID), the blindspots, what the next month starts
  with.
- **The registers** (`docs/decision-register.md`, `docs/blindspot-register.md`)
  and the rules are where a lesson becomes durable; the logs are where it is
  found. `tools/archaeology` reads all of them.

## What a blindspot entry owes

From entry 52 on, an entry names its guard -- the tool, hook, rule or suite
that now catches the shape -- in backticks, and the guard exists in the tree
when the entry is committed. An entry that ends in "be more careful" is not
an entry; `working-principles.md` says a rule broken twice moves up a stage,
and the stage above "written" is "audited". If no tool can catch it, the
entry says so in those words, and that sentence is the guard the check
accepts as honest.

## What a friction entry is

One line, the moment the work slowed: what slowed it, what would have
caught it, and the issue or guard. The mini-retro's second question ("what
was harder than expected?") is answered from this file. An entry without an
issue expires in three days and refuses the next push, which is the point:
a friction nobody owns is a blindspot in waiting. Filing the issue follows
D-QA-012 (the maintainer's words quoted, the same session).

**Every lane writes its own line, the moment the work slows (D-WORKFLOW-253,
#1508).** The one-on-one steward included: no lane waits for another to be
free, or for the end of the work. On 2026-11-27 Max asked three times in
eleven minutes for the day's friction to be logged while the lane that kept
the log was stopped on a usage limit, and four stops had no line: *"Let's
make sure all frictions are logged. We need this to be standard practice."*
The OS coordinator reads each line it finds before committing it on `next`
-- six went in once unread -- and gives it its issue or guard within the three
days. A failed run and a stopped chain leave a stub line by machine for a
lane to complete: `tools/friction-stub`, called by `tools/watch-build` on a
build's non-zero rc, by `tools/vm-qa` on a FAIL, and by `tools/chain-lib`'s
`stop` (#1508). A stub ends `issue: none`; whoever reads it writes what slowed
the work and what would have caught it, or says the stop was deliberate, and
gives it its issue. A failure no tool writes for -- a lane's own stop, a proof
run by hand -- still has its line written by the lane that reads it, with the
failure's own time.

## Running it

```bash
tools/ceremony-check          # the full report; exit 1 when anything is overdue
tools/ceremony-check --gate   # what the push guard runs
tools/archaeology <terms>     # before anything is called pending or new
tools/work-log-index --write  # after a work-log entry
```

The fork CI (`.github/workflows/fork-checks.yml`) runs the index check, the
register lint and `ceremony-check` on every push of `next` and daily, so a
ceremony owed shows as a red badge until its artifact exists. `fork-*`
workflows never reach an upstream PR (`fork-workflow.md`).

## When the CI itself goes quiet (#1450)

A CI-red ceremony works only while the CI runs. GitHub stopped starting the fork's workflows on 2026-10-29 and sent nothing. Because the record checks were red on most days by design, a missing run looked like every other day, and the stop was found 26 days later (#1446). Max, 2026-11-24: *"why'd this go unnoticed? How can we have better alerts about when we have problems like this pop up?"*

`tools/ci-silence-check` asks GitHub five things:
- whether the newest push of `next` got a check suite (FAIL after a 10-minute grace);
- whether the fork's own `fork-checks.yml` ran in the last 26 hours (upstream's scheduled workflows start daily on the fork and fail or skip, so they do not count);
- whether the repository's public Actions page carries GitHub's pause banner. The cause of #1446 was there and nowhere else: *"Workflows are not currently being run on this fork due to the scale of GitHub Actions usage. A repository maintainer can choose to re-enable these."* The API does not expose it, so the tool fetches the page signed out;
- whether the newest completed fork record checks run is red because of a **guard**, which is FAIL and means act;
- or red only because a **record is owed**: an audit, a futro or a checkbox sweep from the table above. That is OWED, never a failure by itself.

The volume behind the pause was the fork's own wordlist check: 988 of the last 1,000 October runs. It runs on every push of every branch (D-WORKFLOW-061), so its cost per run is what is kept small. Its tree scan greps in batches, not once per file, and its checkout is treeless.

`fork-checks.yml` runs the two kinds as separate jobs, `guards` and `records`, so the run itself shows which kind of red it is. When GitHub cannot be read it exits 2, which is not a pass. The push guard prints its verdict for the head a push of `next` replaces. It warns but does not refuse, because an outage on GitHub's side must not stop the record from being pushed.

## Execution discipline

Recurring approval or handoff stalls trigger a focused mini-retro at the next
useful checkpoint, even when a delivery phase has not ended (D-WORKFLOW-184,
#1434). Name this an incident/process review, not product phase completion.
Use the retained timeline, prior decisions and actual artifacts; distinguish
missing guidance from undiscovered or bypassed guidance. Give every adjustment
an owner, changed rule/tool/issue, and next real outcome that could disprove it.
Review that outcome at the next relevant return and in the weekly summary.

Before the next consequential delivery step, use a proportionate futro to
check remaining assumptions and likely failure paths. Reuse accepted source
reviews and existing plans. Run dependent ceremony stages serially, while
independent authorized preparation continues in other lanes. These focused
reviews add no generic human approval, duplicate audit or new build gate;
the established calendar and push checks above still apply. A written lesson
is implementation evidence, not evidence that recurring delays improved.

The delivery, futro and mini-retro skills consume settled outputs from the
preceding stage. Run their stages serially under one orchestrator; another
session must not mutate the same scope concurrently. Delegation within a stage
requires that stage's authorization. A resume continues from recorded evidence;
it does not rerun completed ceremonies or request an already granted approval.
The milestone body and `milestone-phase-naming.md` determine the current phase.
