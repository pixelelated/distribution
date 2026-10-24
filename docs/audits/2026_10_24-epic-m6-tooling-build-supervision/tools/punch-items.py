#!/usr/bin/env python3
"""05-punch-list.md from one list (#656): the items, the punch_index and the Phase 7 table.
    python3 -I punch-items.py > 05-punch-list.md
"""
HOST = "No guest needed: host-side tools; the proof is an isolated control in the lane's worktree with synthetic inputs, never the real host action (brief § 2)"
AWN = "nothing on devices or in clouds: these are build-host tools; what they leave is under `.build-runs/`, `.git/pixelelated-build-admission/`, `/tmp` or the host's own configuration, named in the item"
I = [
 dict(f="F-01", tracked="#913", t="three recorded watcher controls have failed since the admission guard (2026-10-13), on two layers, and none runs in the fork CI", sev="Medium", cat="Interaction Defect", q="Q3",
  area="the controls: `docs/qa-logs/2026-10-04-watch-progress/test-progress.py`, `test-watch-build.py`, `docs/qa-logs/2026-10-05-watch-submit/test-submit.py`",
  what="The fixtures copy no `build-admission` (layer 1), and their payloads carry neither an admission nor `--record-only` (layer 2, `watch-build:96-98`). Prepare an admission through `admission-test-fixture.py`, as `test-build-monitor` does, or use `--record-only` for record-shaped cases; prove each control fails with the admission step removed; add the three to `fork-checks.yml`.",
  where="`test-progress.py:39-40`, `test-watch-build.py:56-57`, `test-submit.py:17-18`; `tools/watch-build:50-51`, `:96-98`; `.github/workflows/fork-checks.yml:42-44`",
  ev="P2 (the controls and diagnostics), P10 (pass at `d7e2d6be41^`, fail at `d7e2d6be41`)", vm=HOST, aw="nothing inherited: the controls write only to their own temporary roots", bug=True,
  acc="each of the three exits 0 at the fix; a copy without the admission step fails; the three run in `fork-checks.yml`; outputs quoted on the bug."),
 dict(f="F-02", t="`test-submit.py` leaves its `mkdtemp` directory under `/tmp` on every run", sev="Low", cat="Code Quality", q="Q3",
  area="the control `docs/qa-logs/2026-10-05-watch-submit/test-submit.py`", what="Remove the temporary root in a `finally`, as the other controls do.",
  where="`test-submit.py:15`", ev="P6; the `/tmp` count 4 → 10 over passing and failing runs", vm=HOST,
  aw="ten `/tmp/pixelelated-watch-submit-*` directories on 2026-10-24 (six of them this lane's runs); nothing reads them",
  acc="the count of `/tmp/pixelelated-watch-submit-*` is equal before and after a run, quoted.", tracked="#913"),
 dict(f="F-03", tracked="#914", t="`build-preflight --stop-vms` stops every same-UID process matching `qemu-system-x86_64` by plain `kill`, unowned and unwaited; a failed census reads as none", sev="Medium", cat="Interaction Defect", q="Q3",
  area="`tools/build-preflight`", what="Stop only owned guests through `tools/vm-stop` (identity, owned disk, wait for exit), or remove `--stop-vms` and point at `tools/vm-stop`; make a failed `pgrep` an error, not \"no guests\" (G-47); compare the swap threshold exactly, as the helper does (G-48). The flag's contract is the coordinator's.",
  where="`tools/build-preflight:101-123`, `:67`, `:93`", ev="P8; the seat's G-47 and G-48", vm=HOST,
  aw="nothing persistent; whether a past `--stop-vms` ever ended another lane's guest is not in the record", bug=True,
  acc="a control with fake guests shows an unowned guest left running with a nonzero verdict, an owned guest stopped and awaited, a failed census an error, and READY only after exit; the threshold matches the helper's at the boundary."),
 dict(f="F-04", tracked="#915", t="the admission and retention tools need Python 3.11 (`hashlib.file_digest`); the container runs 3.10, so an admitted docker-shell build tracebacks", sev="Medium", cat="Interaction Defect", q="Q1",
  area="`tools/host-maintenance/build-admission`, `retention-report`, `tools/watch-build`", what="Hash with a streamed `hashlib.sha256()` loop (as #492's fix did); make the admission path's failures reach `watch-build`'s refusal (`ValueError`, or the except tuples widened).",
  where="`build-admission:34`, `retention-report:22`, `:69`; `watch-build:190`, `:221`; `build-admission.md:101-102`", ev="P5; the seat's re-grade", vm=HOST + "; the pinned image's Python is the interpreter to prove it under, a read-only container start the coordinator may authorize",
  aw="nothing inherited: all 664 recorded admissions carry the host's PID namespace (`4026531836`); no docker-shell admission was ever made", bug=True,
  acc="a fixture file hashes equal under Python 3.10 and 3.14; a deliberately broken digest gives `watch-build: <reason>`, rc 2, not a traceback; quoted."),
 dict(f="F-05", tracked="#916", t="`watch-job` reports `died` for any process whose identity it cannot read, where #506's rule says an unreadable PID is unknown", sev="Low", cat="Code Quality", q="Q3",
  area="`tools/watch-job`", what="Distinguish \"cannot read\" from \"exited\": an identity unreadable at start, or a `kill -0` refused for permission, gives `error` (or an `unknown` the reader cannot mistake for death), never `died`.",
  where="`tools/watch-job:163-171`, `:218-233`", ev="the trace; the seat's broadening", vm=HOST + "; a PID hidden by an unprivileged `unshare` namespace is the input",
  aw="nothing inherited: every one of the 1,885 recorded statuses is `finished`; none says `died`", bug=True,
  acc="a control with a PID the watcher cannot read gets a non-`died` state; a control whose job truly dies still gets `died`; both quoted."),
 dict(f="F-06", tracked="#917", t="the runner's end-of-run and failure paths: a late watcher skips `finish`, a failed log write orphans the payload, a cancellation during admission still launches, a stalled console blocks the build", sev="Low", cat="Code Quality", q="Q3",
  area="`tools/watch-build`", what="Cover the second `monitor.wait` timeout with a recorded finish (F-06); kill the child before writing to a failed log (G-27); check `interrupted` before `Popen` (G-30); bound the console write or drop the console on backpressure (G-28).",
  where="`tools/watch-build:202-214`, `:176-198`, `:153-170`, `:180-187`", ev="the trace; the seat's G-27 to G-30", vm=HOST,
  aw="nothing inherited: no recorded run holds a `runner-error` or lacks a terminal status among the 1,885", bug=True,
  acc="a control with a watcher that will not exit records the runner's result; a control whose log write fails leaves no live payload; a signal during admission starts no payload; each quoted."),
 dict(f="F-07", tracked="#918", t="the worktree lock ends with the runner, so after an outright kill a second build can start beside the orphaned command", sev="Medium", cat="Interaction Defect", q="Q3",
  area="`tools/watch-build`", what="Hold exclusion for the command's lifetime: an inherited lock descriptor in the command, or a refusal while an earlier run's `command.pid` group is alive. Isolate the lock in its control, with a fresh admission for the second launch.",
  where="`tools/watch-build:102-106`, `:165-167`; `test-build-monitor:219-226`", ev="the trace; the seat's re-grade and its reading of the control", vm=HOST,
  aw="nothing inherited: the fix changes the next launch; the record was not searched for concurrent runs in one worktree", bug=True,
  acc="a control kills a runner whose command is alive, then a second admitted launch in the same worktree is refused; the lock control uses a fresh admission; both quoted."),
 dict(f="F-08", t="73 guards wired, of which 23 have no running control and 3 only partial ones; five `yes` rows were credited to controls that do not construct their failure", sev="Medium", cat="Renovation", q="Q6",
  area="the eighteen files' controls", what="A control per `none` row, beside the stream that touches the tool, or one Renovation stream; correct the misattributed rows' controls (14 isolate the lock, 16 a stale heartbeat, 31 the report digest).",
  where="`04` § Q6, rows 12 to 73", ev="P7; the seat's refutation of the table", vm=HOST, aw=AWN,
  acc="each `none` row names a control that fails when its guard is removed, or is withdrawn with its reason; the table re-read."),
 dict(f="F-09", t="the legacy layout in `fork-newdrive:20-21` and `watch-job:36`", sev="Low", cat="Renovation", q="Q1",
  area="`tools/fork-newdrive`, `tools/watch-job`", what="#640's rows: the paths follow the layout move; unchanged here (futro A5).",
  where="`tools/fork-newdrive:20-21`, `tools/watch-job:36`", ev="the lines quoted in `04` § Q1", vm=HOST, aw=AWN,
  acc="#640 carries both rows; the lines unchanged on this branch."),
 dict(f="F-10", t="`fork-newdrive`, a one-time migration, carries stale and unsafe steps: its header partitions the device its own usage calls the OS disk", sev="Medium", cat="Renovation", q="Q6",
  area="`tools/fork-newdrive`", what="Retire it, or quarantine it behind an explicit archival notice: the header's destructive commands (G-49), discovery errors read as false (G-50), no rollback (G-51), no quiescence check (G-52), a hardcoded `ext4` (G-53), the detached-worktree fallback and `sudo rm -rf` advice. The coordinator's call, with #640.",
  where="`tools/fork-newdrive:12-15`, `:31-35`, `:40-55`, `:100-154`", ev="the seat's G-49 to G-53; the reading", vm=HOST, aw=AWN,
  acc="the tool is removed or marked archival with its header's commands gone; or each step is guarded, with a control; the coordinator's disposition recorded."),
 dict(f="F-11", t="(withdrawn) the README's memory-guard-removed control", sev="Low", cat="Code Quality", q="Q7",
  area="`tools/host-maintenance/README.md`", what="Withdrawn at stage C: `test_insufficient_memory_and_boundary` fails when the refusal is removed.",
  where="`README.md:95-101`; `test-swap-reclaim:199-206`", ev="P9; the seat's refutation", vm=HOST, aw=AWN, acc="none: withdrawn."),
 dict(f="F-12", tracked="#919", t="admission reservations live per clone, so two clones on one volume each admit against the same free bytes; true on this host", sev="Medium", cat="Interaction Defect", q="Q3",
  area="`tools/host-maintenance/build-admission`", what="Key the registry by filesystem (a registry on the measured volume, or a host-wide path), or refuse when another clone's registry on the same device holds unconsumed reservations. A contract question for the coordinator; the defect is the fork's.",
  where="`build-admission:77-80`, `:165-168`, `:202-204`", ev="P12; the seat's G-12", vm=HOST,
  aw="M7's registry under `/workspace/repos/rocknix/.git/pixelelated-build-admission/` holds its reservations; the M6 clone has none; a fix reads the existing registry, migrating nothing", bug=True,
  acc="a control with two clones on one filesystem refuses the second admission when the first's unconsumed reservation leaves too little; quoted."),
 dict(f="F-13", t="the installer installs, as root, the helper bytes beside it in a user-writable checkout, with no expected digest; not crash-atomic; its final check is an `assert`", sev="Medium", cat="Interaction Defect", q="Q3",
  area="`tools/host-maintenance/install`", what="A lead for the coordinator (D-INFRA-015 is the owner's): bind the reviewed helper's digest (a constant the administrator reviews, or a staged root-owned copy), replace the `assert` with an explicit check (G-11), and say what a SIGTERM leaves (G-10).",
  where="`install:160-168`, `:106-157`, `:120`", ev="the seat's G-08, G-10, G-11, narrowed", vm=HOST + "; never a real installation",
  aw="the installed helper and policy on serval (2026-10-04 rollout, `docs/qa-logs/2026-10-04-host-swap-rollout/installed.json`) stay as they are; nothing here touches them",
  acc="the coordinator's disposition recorded on this audit; if a stream: a control installs into a temporary root and refuses a helper whose digest differs."),
 dict(f="F-14", tracked="#920", t="`retention-report` binds a plan hash taken after the scan, starts its freshness after the scan, and sums reclaim across filesystems", sev="Low", cat="Code Quality", q="Q3",
  area="`tools/host-maintenance/retention-report`", what="Read the plan's bytes once and hash those (G-40); stamp the observation start and let admission's window run from it (G-41); count only candidates on `volume` (G-45).",
  where="`retention-report:305-308`, `:293`, `:287`", ev="the seat's G-40, G-41, G-45", vm=HOST,
  aw="earlier reports stay valid for their 900 s and then expire; nothing inherited", bug=True,
  acc="a control that edits the plan during a scan gets a mismatch; the report carries its observation start; quoted."),
 dict(f="F-15", t="`test-retention-report` reads the real `/proc` and Docker, so a live QEMU on the host flips its positives", sev="Low", cat="Code Quality", q="Q3",
  area="`tools/host-maintenance/test-retention-report`", what="Inject the process and container observations as `test-build-admission`'s recovery cases do, so the control is isolated from the host.",
  where="`test-retention-report:37-43`; `retention-report:172-198`", ev="the seat's G-46", vm=HOST, aw=AWN, tracked="#913",
  acc="the control passes with a QEMU process present on the host (a fake one in its own namespace), quoted."),
 dict(f="F-16", tracked="#921", t="`consume` trusts the run's own `admission.json` over the registry row, and writes its receipt before the registry commits", sev="Low", cat="Code Quality", q="Q3",
  area="`tools/host-maintenance/build-admission`", what="Compare the whole registry row as recovery does (G-22); commit the registry first, or reconcile an existing `admission-consumed.json` on retry (G-26).",
  where="`build-admission:245-282`, `:440`", ev="the seat's G-22, G-26", vm=HOST,
  aw="664 recorded admissions; the fix reads their existing rows and receipts unchanged", bug=True,
  acc="a control with an edited `admission.json` is refused; a control with a failed registry commit retries to `consumed`; quoted."),
 dict(f="F-17", tracked="#922", t="`reclaim-swap` defers only three signals: a SIGQUIT during `swapoff` leaves swap off; its flushed print sits between check and mutation", sev="Low", cat="Code Quality", q="Q3",
  area="`tools/host-maintenance/reclaim-swap`", what="Block every catchable terminating signal around the mutation (SIGQUIT, SIGUSR1, SIGUSR2, SIGALRM, SIGPIPE), and print before the final checks (G-06, G-03). A change to the installed helper needs the owner's reinstallation (D-INFRA-015).",
  where="`reclaim-swap:20`, `:157-184`", ev="the seat's G-06, G-03", vm=HOST + "; `test-swap-reclaim`'s doubles only, never a real swap command",
  aw="the installed helper on serval is unchanged until the owner reinstalls", bug=True,
  acc="a double-driven control delivers SIGQUIT during `swapoff` and sees reactivation verified; quoted."),
 dict(f="F-18", t="`watch-job` passes the caller's pattern and status names unguarded to `grep` and `mv`, and writes derived names it never resolved", sev="Low", cat="Code Quality", q="Q2",
  area="`tools/watch-job`", what="`grep -E -e \"$PATTERN\"` and `--` before paths; resolve the `.pid` and `.tmp` names into the overlap check.",
  where="`watch-job:107-108`, `:160`, `:216`, `:262`, `:266`", ev="the seat's G-33, G-34", vm=HOST, aw=AWN, tracked="#916",
  acc="`--pattern --help` is refused or matched literally; a status name starting with `-` works; quoted."),
 dict(f="F-19", tracked="#923", t="`watch-build-submit`'s fresh-owner check misses its own receipts, it starts the worker before its pid receipt, and the worker forwards no signal", sev="Low", cat="Code Quality", q="Q3",
  area="`tools/watch-build-submit`", what="Check every launcher receipt name before reserving (G-36); write `launcher-pid.json` before or atomically with the start (G-37); forward termination to the runner and record it (G-38).",
  where="`watch-build-submit:69-71`, `:83-89`, `:30-50`", ev="the seat's G-36 to G-38", vm=HOST, aw=AWN, bug=True,
  acc="a control with a stale `launcher-result.json` in the owner is refused; a signal to the worker reaches the runner and is recorded; quoted (F-01's repaired `test-submit.py` carries them)."),
 dict(f="F-20", t="`fork-publish-release`: byte binding rests on the candidate store's immutability, and a SIGTERM orphans the state check", sev="Low", cat="Code Quality", q="Q3",
  area="`tools/fork-publish-release`", what="A lead for the coordinator: the store is outside this slice (G-54); the orphan (G-55) wants a signal handler that ends the group.",
  where="`fork-publish-release:22-24`, `:89-97`, `:113`", ev="the seat's G-54, G-55", vm=HOST, aw=AWN,
  acc="the coordinator's disposition recorded; if a stream, a control sends SIGTERM during the check and finds no orphan."),
 dict(f="F-21", t="the admission's operational-guard boundaries the seat named: registry history, the bearer marker, nested redirection, output overlap, metadata identity, read-then-hash, escaped sessions, the report's lexical containment and PID view", sev="Low", cat="Renovation", q="Q6",
  area="`tools/host-maintenance/build-admission`, `retention-report`, `tools/watch-build`", what="Leads for the coordinator: each is a contract question for a guard the guide calls operational, not a security boundary (`build-admission.md:9-10`).",
  where="`04` § Second opinion, G-13 to G-19, G-21, G-25, G-42 to G-44", ev="the seat's items, narrowed", vm=HOST, aw=AWN,
  acc="each lead dispositioned by the coordinator: a contract row, a stream or a recorded acceptance."),
]

P7 = {   # (outcome, evidence, proved) by F; filled at Phase 7
 "F-01": ("Resolved", "resolved:`9b071c5d12` (#913, S1): the three controls prepare an admission; P13. The CI clause is deferred:#657 (`fork-checks.yml` is T10's)", "fix-control"),
 "F-02": ("Resolved", "resolved:`9b071c5d12` (S1): `test-submit.py` removes its root at exit; `/tmp` 10 before and after; P13", "fix-control"),
 "F-03": ("Resolved", "resolved:`c9e38e2939`, `c4d4c147d0` (#914, S2, D-INFRA-028): the preflight stops nothing and names `tools/vm-stop`; P14", "fix-control"),
 "F-04": ("Resolved", "resolved:`6a25254359`, `86ef7ae6b1` (#915, S3 and its addendum): a streamed hash, proved under the pinned 3.10.12; a refusal logged as one; P16, P20", "fix-control"),
 "F-05": ("Resolved", "resolved:`4a22ed0b41` (#916, S4): an unreadable PID is an observation error; the namespace limit is #506's; P15", "fix-control"),
 "F-06": ("Resolved", "resolved:`dce53bf0ba` (#917, S5): four end-of-run cases; P17", "fix-control"),
 "F-07": ("Resolved", "resolved:`d1a1495bc5` (#918, S5): the command inherits the lock; P17", "fix-control"),
 "F-08": ("Deferred", "deferred:#925 for the `none` rows no stream reached; the streams' controls close their rows, and the five misattributed rows are corrected in `04` § Q6 (S5, S6)", ""),
 "F-09": ("Deferred", "deferred:#640, the legacy-layout rows (brief § 2; futro A5); after S8 its `fork-newdrive:20-21` row is moot (said on #640)", ""),
 "F-10": ("Resolved", "resolved:`ad70390f60`, `00e571b8a8` (S8, D-INFRA-030): retired; its index row and personal-paths entry leave with `.githooks/pre-push`'s pattern (#657); P21", "fix-tree"),
 "F-11": ("Withdrawn", "withdrawn at stage C: `test_insufficient_memory_and_boundary` (`test-swap-reclaim:199-206`) is the retained control; the seat's refutation, `04` § Second opinion", ""),
 "F-12": ("Resolved", "resolved:`e03fc7982d` (#919, S6, D-INFRA-029): one registry per filesystem in the user's state directory; P18", "fix-control"),
 "F-13": ("Deferred", "deferred:#927, the installer's digest, assert and interruption (an `Ops:` lead for the owner, D-INFRA-015); never a real installation here", ""),
 "F-14": ("Resolved", "resolved:`82840dbc42` (#920, S6): the plan bytes read are hashed, `observation_start`, reclaim on the volume; P18", "fix-control"),
 "F-15": ("Resolved", "resolved:`a9bd346d54` (S1): `test-retention-report` reads a fixture `/proc` and no daemon; P13", "fix-control"),
 "F-16": ("Resolved", "resolved:`e8828c13ad` (#921, S6): the whole row compared; the registry committed first; P18", "fix-control"),
 "F-17": ("Resolved", "resolved:`39d9fc1e04` (#922, S7): eight signals deferred; the installed copy changes when the owner reinstalls (D-INFRA-015); P19", "fix-control"),
 "F-18": ("Resolved", "resolved:`4a22ed0b41` (#916, S4): `-e` and `--` before every caller value; derived outputs resolved; P15", "fix-control"),
 "F-19": ("Resolved", "resolved:`c1e799b3b5` (#923, S7): every receipt checked, the pid receipt first, termination forwarded; P19", "fix-control"),
 "F-20": ("Deferred", "deferred:#528, whole: the release preparer's store and orphan, with the seat's G-54 and G-55", ""),
 "F-21": ("Deferred", "deferred:#926, one lead per letter, to be dispositioned with the owner as contract rows", ""),
}

def main():
  out = ["# Punch List — M6.P2 T9, build supervision and host maintenance", "",
         "**Independent depth** (D-WORKFLOW-184): one GPT-6 Astra seat, graded in `04` § Second opinion. Every `where` is at `8ebaf8daad`. The audit issue is #924 (a sub-issue of #656); the bugs are #913 to #923. Generated by `tools/punch-items.py` from one list, so the items, the `punch_index` and the Phase 7 table agree.", "", "---", ""]
  idx = ["```yaml", "punch_index:"]
  gate = ["## Phase 7 resolution gate", "", "| Item | Outcome | Evidence |", "| --- | --- | --- |"]
  for n, x in enumerate(I, 1):
      pl = f"PL-{n:02d}"
      out += [f"## {pl}: {x['t']}", "", f"- **Severity:** {x['sev']}", f"- **Category:** {x['cat']}", f"- **Question:** {x['q']}", f"- **Source Finding:** {x['f']}", f"- **Owner area:** {x['area']}", f"- **What:** {x['what']}", f"- **Where:** {x['where']}", f"- **Evidence:** {x['ev']}", f"- **Can this be done on the VM?** {x['vm']}", f"- **Already written:** {x['aw']}", f"- **Acceptance:** {x['acc']}"]
      if x.get("bug") or x.get("tracked"): out.append(f"- **Bug issue:** {x.get('tracked', 'filed at stage D')}")
      out.append("")
      idx += [f"- id: {pl}", f"  severity: {x['sev']}", f"  category: {x['cat']}", f"  question: {x['q']}", f"  source_finding: \"{x['f']}\"", f"  owner_area: \"{x['area'].replace(chr(34), chr(39))}\""]
      if x.get("bug") or x.get("tracked"): idx.append(f"  tracked: \"{x.get('tracked', 'bug issue filed at stage D')}\"")
      p7 = P7.get(x["f"])
      if p7:
          idx.append(f"  outcome: \"{p7[0].lower()}\"")
          if p7[2]: idx.append(f"  proved: \"{p7[2]}\"")
          gate.append(f"| {pl} | **{p7[0]}** | {p7[1]}{'; ' + p7[2] if p7[2] else ''} |")
      else:
          idx.append("  outcome: open")
          gate.append(f"| {pl} | Open | stage D files the issue; a stage-E stream brief or the coordinator's disposition resolves |")
  idx.append("```")
  print("\n".join(out + ["## Machine-readable index", ""] + idx + [""] + gate))

if __name__ == "__main__":
    main()
