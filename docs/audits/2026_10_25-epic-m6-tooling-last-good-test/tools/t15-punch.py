#!/usr/bin/env python3
"""t15-punch.py -- T15's punch list, from one list: 05-punch-list.md (the
items, the punch_index YAML, the Phase 7 table) and, with --bugs DIR, one bug
body per item that carries a bug. Run from the lane worktree.
  python3 -I docs/audits/2026_10_25-epic-m6-tooling-last-good-test/tools/t15-punch.py [--bugs DIR]
"""
import os, sys
A = "docs/audits/2026_10_25-epic-m6-tooling-last-good-test"
F = "tools/last-good-scripts-test"
VM = ("**Can this be done on the VM?** No guest is needed: the suite runs on the build host by design, its scripts in `bwrap` "
      "sandboxes against fixtures. The proof is the file's own new or re-run case, which fails on the unfixed file and passes "
      "on the fixed one, run under the M7 image's busybox through `QA_SYSTEM_ROOT` (and, where the defect is the fallback, "
      "with it unset).")
I = [
 dict(id="PL-01", sev="High", cat="Correctness", q="Q2", src="F-01, F-20; the seat's Q1", bug=True,
  title="last-good-scripts-test runs on the host's busybox (or none) when no build root is found, and its verdict never says so",
  where=f"`{F}:381-401` (`:400` `command -v busybox || true`), `:416-426`; `:8777-8779`, `:8809-8811` (the G-B-15 probes accept any BusyBox banner); the verdict `:14235-14238`",
  what="With `QA_SYSTEM_ROOT` unset and no build root under the three globs, which reach none of the M7 roots, the suite copies the host's busybox (1.37.0 here) and judges the scripts with it. The banner at `:426` names the copy; the verdict says `PASSED` or `N CHECK(S) FAILED` without saying whose applets judged. From every M6 worktree: 319 FAIL, all the busybox's (`bbhost` 319, `rchost` 0), with `flock` the only refusal named. With no busybox at all: no copy, no wrappers, no banner, GNU tools, blindspot 34's exact case. #1015's root cause.",
  acc=["at `fixed-at`, a run from a worktree with no build root and `QA_SYSTEM_ROOT` unset refuses (exit 2, naming what it lacks and how to supply it) or, in an explicitly requested host-diagnostic mode, marks every result line and ends with a verdict that says it is not device evidence (exit 3): the run's output quoted in `02` (the stream's new case)",
       "a run with `QA_SYSTEM_ROOT` on a named M7 root's `image/system` reaches its verdict with the busybox's provenance (path, version, BUILD_ID) in the final lines, not only the banner: quoted in `02`",
       "the G-B-15 probes (`:8777-8811`) check the busybox's provenance, not only the word BusyBox: a constructed host-busybox run fails them (the stream's case)"],
  aw="Every recorded run from an M6 worktree (T12's three, T14's, this slice's run 2) judged the host's busybox; their FAILs stand in the record as host evidence, and #1015 carries the attribution. Nothing on a device."),
 dict(id="PL-02", sev="High", cat="Correctness", q="Q3", src="F-07, G-10", bug=True,
  title="last-good-scripts-test's writer-test calls pass a busybox T14's contract refuses, and flatten the child's CANNOT and unverified exits into FAIL",
  where=f"`{F}:14221-14233` (`ag`, `ah`), `:310`; the callees at T14's `7c1d729b57`",
  what="`ag` and `ah` call `settings-modes-test` and `melonds-upgrade-test` with `--busybox \"${BB_HOST}\"`, the run's own scratch copy, which T14's S8 contract (#997, `7c1d729b57`) refuses unless told `--busybox-from <BUILD_ID>` or `--unverified-busybox`. And `check $?` (`:310`) counts every non-zero child exit as a FAIL, so the child's CANNOT (2) and unverified (3) become reported regressions.",
  acc=["at `fixed-at`, `grep -n -E 'busybox-from|unverified-busybox' tools/last-good-scripts-test` prints both call sites: `--busybox-from <BUILD_ID>` when `QA_SYSTEM_ROOT` or a build root supplied the busybox, `--unverified-busybox` when the host did",
       "a child's exit 2 and exit 3 are carried to the suite's verdict as cannot-run and unverified, not as FAIL: a constructed child that exits 2, then 3, gives the suite the matching verdict (the stream's case)",
       "with T14's tools merged, `ag` and `ah` PASS in a run with `QA_SYSTEM_ROOT` on a named M7 root: their lines quoted"],
  aw="T14's own run of this file (2026-10-24, its hand-back) showed both calls refused; nothing is written by them on a device."),
 dict(id="PL-03", sev="Medium", cat="Correctness", q="Q4", src="F-02", bug=True,
  title="last-good-scripts-test's stream A takes the host's rclone when no build root is found, and never asserts its version",
  where=f"`{F}:8906-8914`",
  what="`SA_RCLONE_SRC=$(image_tool_source rclone version)` falls back to the host's `/usr/bin/rclone` (v1.60.1-DEV here, against the recipe's 1.75.2) as the busybox does; the version is printed at `:8914` and never asserted. Measured: `rchost` (the image's busybox with the host's rclone 1.60.1) passes 1,313/0, so no case would notice.",
  acc=["at `fixed-at`, stream A refuses, or marks as unverified, an rclone not taken from `QA_SYSTEM_ROOT` or a build root, and asserts `rclone version`'s first line equals the recipe's `PKG_VERSION`: a run with the host's rclone in a constructed root is refused or marked (the stream's case)"],
  aw="Every stream-A run from an M6 worktree used the host's rclone; the record's verdicts stand as host evidence. Nothing on a device."),
 dict(id="PL-04", sev="Medium", cat="Correctness", q="Q2", src="F-03 (the coordinator, 00:36 UTC)", bug=True,
  title="last-good-scripts-test reads earlier builds' files from git with the failure silenced, so a history-less checkout makes an empty fixture",
  where=f"`{F}:3205-3215` (`f1_tree_at`: `ls-tree ... 2>/dev/null | while ...; exit 2` in the pipeline's subshell), `:4271` (`git show 417dcd8610:... 2>/dev/null`)",
  what="In an export or a shallow clone without `417dcd8610` or `73b20caf86`, the read fails silently, the fixture is empty, and only the downstream vacuity detectors catch it, ten checks later. The coordinator's run from an export failed exactly those ten.",
  acc=["at `fixed-at`, a run from an export without `.git` stops at the read with exit 2, naming the ref and the path it could not read (the stream's case: the export run's output quoted)",
       "the same run from the worktree passes the `F1.`, `F1r.` and `C.` checks as before: their lines quoted"],
  aw="Nothing written on a device; the coordinator's export run's ten FAILs stand as the record of the shape."),
 dict(id="PL-05", sev="Medium", cat="Correctness", q="Q3", src="F-04 (the coordinator, 02:24 UTC)", bug=True,
  title="last-good-scripts-test's header names two --old refs that no longer exist",
  where=f"`{F}:185` (`0f7785e6ed`), `:191` (`d79281066c`)",
  what="Both refs are invalid in this repository (`git cat-file -t`: *Not a valid object name*; no branch contains them), so q's control and p's pending/flushed control cannot run. They were written by `1a5c066623` (#166) and `67a89cb623` (#173); the intended trees are those commits' parents, `717bc04449` and `51e2acece6`.",
  acc=["at `fixed-at`, the header names `717bc04449` and `51e2acece6` (or the refs the run proves), and `BASE_REF=<each> tools/last-good-scripts-test --old` fails the checks the header promises (q's; p's pending and flushed): the runs' outputs quoted"],
  aw="Nothing on a device."),
 dict(id="PL-06", sev="Medium", cat="Correctness", q="Q3", src="F-05 (the coordinator, 02:24 UTC); the seat's Q4", bug=True,
  title="last-good-scripts-test --old ends the whole run at the first script a ref predates, so no recipe reaches a verdict",
  where=f"`{F}:320-325` (`src_of`)",
  what="Under `--old`, `src_of` exits 2 for the whole run when a script is absent at `BASE_REF`. All twelve recipes stop: two at once (PL-05), ten at `s` (`rocknix-evidence`) or `x` (`rocknix-corekeep`), so sections from there to `ah` never run as controls. The coordinator's fix: a section whose script is absent at the ref is NOT APPLICABLE and the run goes on. The seat's distinctions, to keep: an invalid ref or unreadable required input stays CANNOT (exit 2); an absent historical feature the header promises as a FAIL stays a FAIL; a selected check that cannot run is incomplete, never PASS.",
  acc=["at `fixed-at`, `BASE_REF=1d1503180d tools/last-good-scripts-test --old` reaches its verdict (exit 1, its FAILs counted) with the sections whose scripts the ref predates reported NOT APPLICABLE by name: its output quoted",
       "an invalid `BASE_REF` still exits 2 at once, naming it: quoted",
       "each of the twelve recipes is run once at `fixed-at` and its verdict and FAIL count recorded in `02`"],
  aw="Nothing on a device."),
 dict(id="PL-07", sev="Medium", cat="Correctness", q="Q3", src="F-06 (the coordinator, 02:24 UTC)", bug=True,
  title="last-good-scripts-test's 70b6c70ca7 recipe fails on patch application, not on the 012 checks it promises",
  where=f"`{F}:219-225` (the recipe), `:2051-2086` (section `t` takes the client pin from the working tree, the patches from `BASE_REF`)",
  what="At `70b6c70ca7`, `t`'s client cannot be built: the tree's patches 003 to 006 do not apply to the pinned client, so its 43 FAILs are patch failures and none of the five `012` checks runs (0 lines name `012`, against 5 PASS in the baseline).",
  acc=["at `fixed-at`, either `t` builds the client pinned at `BASE_REF` and `BASE_REF=70b6c70ca7 --old` fails `t`'s four `012` checks by name (its output quoted), or the recipe is removed from the header with the reason written beside it"],
  aw="Nothing on a device."),
 dict(id="PL-08", sev="Medium", cat="Correctness", q="Q3", src="F-09", bug=True,
  title="last-good-scripts-test treats a missing download three ways: a FAIL, one SKIP for many checks, or checks silently dropped",
  where=f"`{F}:4004-4008`, `:4296-4297` (FAIL); `:6490-6491` (one SKIP for every webkit patch); `:6649` and the `DT_OK`/`DF_OK` blocks with no `else` (`:7040-7078`, `:10128-10358`); `:11180` (F1r-d without `qemu-img`)",
  what="The same absence (a sources-cache tarball, the pinned client, `qemu-img`) is a FAIL in one place, a single SKIP standing in for every dependent check in another, and a silent omission in a third. On a host without the sources cache, section `D`'s 33 busybox FAILs would read as SKIPs.",
  acc=["at `fixed-at`, every dependency absence takes one rule, counted per dependent check (a SKIP each, or a FAIL each), with no `if` that drops checks without counting them: `grep` for the guarded blocks shows each has its counted branch, and a constructed run with the client tarball hidden reports the dependent checks' count (the stream's case)"],
  aw="Nothing on a device."),
 dict(id="PL-09", sev="Medium", cat="Correctness", q="Q3", src="F-10", bug=True,
  title="last-good-scripts-test's 'rc non-zero and nothing written' checks pass when the script never ran",
  where=f"`{F}` (the seat and the first reader: `:573`, `:594`, `:7912`, `:7934`, `:8246`, `:8258`, `:8271`, `:8352`, `:8583`, `:8787`, `:8828`, `:9172`, `:9744`, `:9951`, `:9957`, `:10085`, `:10580`, `:10727`, `:11050`, `:13270`, `:13508`; the `C.` negatives `:4616`-`:4884` behind `:4610`'s hidden 127)",
  what="A sandbox that cannot start (rc 1 from `bwrap`, or 127 hidden by `2>/dev/null`), a missing applet path or an unlifted function satisfies a check that asserts only a non-zero exit and an absence. Paired positives usually fail beside it, not always.",
  acc=["at `fixed-at`, each such check also requires a witness that the script under test started and reached the guarded step (a marker the shim or script writes), and a constructed run whose sandbox cannot start fails them (the stream's case, for a representative set named in `02`)"],
  aw="Nothing on a device."),
 dict(id="PL-10", sev="Medium", cat="Correctness", q="Q3", src="F-11", bug=True,
  title="last-good-scripts-test's v section joins three runs with ';' so check reads only the last, and drops sa's status before the no -e check",
  where=f"`{F}:3051`, `:3061-3062`",
  what="At `:3051`, `sa ...; is ... && sa ...; is ... && sa ...; is ...; check $?` reads only the last `is`, which can match output an earlier run left. At `:3061-3062`, `sa`'s status is dropped before the *no -e* check.",
  acc=["at `fixed-at`, each case at `:3051` is its own `check`, and `:3061` requires `sa`'s status: a constructed `set_autosave` that writes the third case's output on the first run fails (the stream's case)"],
  aw="Nothing on a device."),
 dict(id="PL-11", sev="Medium", cat="Security", q="Q2", src="F-16", bug=True,
  title="last-good-scripts-test's sandbox passes the caller's environment and the host network to every script it runs",
  where=f"`{F}:9010-9022` (`sa_run`, 150 calls)",
  what="`sa_run` has no `--clearenv` and no `--unshare-net`: exported `RCLONE_*` and `BASH_ENV` reach the scripts, and the host network is reachable. PATH and HOME are overridden and TMPDIR removed; no external access was shown. T14's S2 fixed the same shape in its four tools.",
  acc=["at `fixed-at`, `sa_run` runs with an environment allowlist and no network but loopback, with case-specific exceptions named: a run with `RCLONE_CONFIG`, an `RCLONE_CONFIG_*` remote, `BASH_ENV` and a function exported passes, and a probe script in the sandbox sees none of them and no interface but `lo` (the stream's case, as T14's `sandbox-case.py`)"],
  aw="Nothing on a device; no external connection is recorded."),
 dict(id="PL-12", sev="Medium", cat="Correctness", q="Q2", src="G-01 (the seat)", bug=True,
  title="last-good-scripts-test's section b runs backuptool with the host's tools even when the image's busybox was found",
  where=f"`{F}:522`, `:536-541`, `:566`, `:586-590`",
  what="`b`'s profile sets PATH `/shim:/usr/bin:/bin` and its sandbox binds no busybox or wrappers, so the founding kill/restore tests are host-tools tests regardless of the busybox source.",
  acc=["at `fixed-at`, `b`'s sandbox binds the busybox copy and its wrappers first on PATH, and a constructed busybox-only behaviour (an applet the host lacks) is reached from `b`: its line quoted"],
  aw="Nothing on a device."),
 dict(id="PL-13", sev="Medium", cat="Correctness", q="Q3", src="G-02 (the seat)", bug=True,
  title="last-good-scripts-test's ag runs the subject checkout's settings-modes-test, not the harness's",
  where=f"`{F}:14224` (`${{ROOT}}`), against `:14188`, `:14231` (`${{HARNESS_ROOT}}`) and `--help` `:248-249`",
  what="With `LAST_GOOD_SOURCE_ROOT` set, `ag` runs the verifier from the checkout under test, against `--help`'s promise that the harness is not replaced.",
  acc=["at `fixed-at`, `ag` runs `${HARNESS_ROOT}/tools/settings-modes-test`: `grep -n 'settings-modes-test' tools/last-good-scripts-test` shows it, and a run with `LAST_GOOD_SOURCE_ROOT` naming a checkout without the tool still runs `ag` (the stream's case)"],
  aw="Nothing on a device."),
 dict(id="PL-14", sev="Medium", cat="Correctness", q="Q3", src="G-04, G-08 (the seat)", bug=True,
  title="last-good-scripts-test orders two race checks by sleep, so the scenario they claim need not occur",
  where=f"`{F}:8852-8860` (the corekeeper contention), `:10326-10333` (D29's marker during a top-up; its poll never asserted)",
  what="Both checks wait with `sleep` and polls whose result is not asserted, so a late second handler or a top-up that finishes first satisfies them with broken locking or acknowledgement.",
  acc=["at `fixed-at`, each check holds the first party at a barrier until the second has reached the contended step, and asserts that it did: a constructed broken lock fails each (the stream's case)"],
  aw="Nothing on a device."),
 dict(id="PL-15", sev="Medium", cat="Correctness", q="Q3", src="G-06 (the seat)", bug=True,
  title="last-good-scripts-test's D13b and D13c replay a Python driver's verdict lines and ignore its exit, so a crash drops checks unseen",
  where=f"`{F}:7320-7357`, `:7370-7432`",
  what="The checks pass on whatever verdict lines the driver printed; a crash after the first PASS loses the rest with no FAIL.",
  acc=["at `fixed-at`, each driver's exit is required to be 0 and its verdict IDs to equal the expected set: a constructed driver that raises after its first verdict fails the check (the stream's case)"],
  aw="Nothing on a device."),
 dict(id="PL-16", sev="Low", cat="Correctness", q="Q2", src="F-12", bug=True,
  title="last-good-scripts-test calls check with two arguments at :13826, so a FAIL there aborts under set -u uncounted",
  where=f"`{F}:13826`, `:309-310`, `:270`",
  what="`check` expands `$3` on failure; with two arguments and `set -u` the run aborts before counting. It runs only where the migration engine exists (historical refs).",
  acc=["at `fixed-at`, every `check` call carries three arguments: a static count of `check` calls with fewer prints 0 (the command quoted)"],
  aw="Nothing on a device."),
 dict(id="PL-17", sev="Low", cat="Correctness", q="Q2", src="F-15 (and the seat's :599, :8784)", bug=True,
  title="last-good-scripts-test's negated pipelines pass when the archive or member cannot be read",
  where=f"`{F}:548`, `:599`, `:803`, `:1036-1047`, `:8784`",
  what="`! tar ... | grep -q` with no producer check turns an unreadable archive into a successful absence; `pipefail` alone does not repair a negated pipeline.",
  acc=["at `fixed-at`, each site extracts into an owned file with its status required, then tests grep's no-match status 1 exactly: a constructed missing member fails each (the stream's case)"],
  aw="Nothing on a device."),
 dict(id="PL-18", sev="Low", cat="Correctness", q="Q3", src="F-17 (and the seat's additions)", bug=True,
  title="last-good-scripts-test grades the working tree in some checks under --old",
  where=f"`{F}:845-851` (g), `:887-890` (h), `:903-928` (i), `:2427` (t), `:3999`, `:4291`, `:10344`, `:6481-6485`, `:6505-6507` (C7)",
  what="These read `${ROOT}` directly or the working index, so `--old` grades the current tree among the expected FAILs.",
  acc=["at `fixed-at`, each reads through `src_of` (or the ref's index): under `BASE_REF=1d1503180d --old`, `g` and `i` FAIL or are NOT APPLICABLE by name rather than PASS (the output quoted)"],
  aw="Nothing on a device."),
 dict(id="PL-19", sev="Low", cat="Correctness", q="Q3", src="F-13, F-14, G-03, G-05, G-09", bug=True,
  title="last-good-scripts-test: five checks whose predicate is weaker than their claim",
  where=f"`{F}:1803-1846` (q: `wait`'s status; pre-created markers), `:1781-1789` (q: the working tree's fragment list), `:2086` (t: *each compiled*), `:4553-4559` (the retirement gate's one spelling), `:7771-7776` (D21's modes)",
  what="q reports `wait`'s status as the boot pass's and tests markers the fixture made; q's historical pass enumerates the working tree's fragments; t's PASS text says *each compiled* while compilation cannot fail it; the retirement gate recognizes one install spelling; D21 rejects only `100644` and `none`.",
  acc=["at `fixed-at`, each predicate matches its claim: the pass's own status, the ref's fragment list, compilation required, the gate reading a stated retirement contract, D21 requiring `100755` exactly: a constructed violation of each fails (the stream's cases)"],
  aw="Nothing on a device."),
 dict(id="PL-20", sev="Low", cat="Correctness", q="Q3", src="F-19, G-07", bug=True,
  title="last-good-scripts-test's S3F judges canaries by fixed paths in the host's /tmp and passes when its functions are absent",
  where=f"`{F}:13668-13715`",
  what="A regression that evaluated the canaries writes the host's `/tmp/s3f-*`, which nothing resets, so a stale file fails a later run; empty `conf_valid` extracts compare equal, an absent `sort_settings` is 127 with its status dropped, and `rc=1` matches `rc=127`.",
  acc=["at `fixed-at`, the canaries write under the run's own temp root, and each function's presence and exact status are asserted: a constructed absent function fails each check (the stream's case)"],
  aw="No `/tmp/s3f-*` exists after this slice's runs (`ls`). Nothing on a device."),
 dict(id="PL-21", sev="Low", cat="Correctness", q="Q3", src="F-21", bug=True,
  title="last-good-scripts-test's PL-022 case measures whatever busybox ran as 'the image's busybox unzip'",
  where=f"`{F}:13399-13424`",
  what="The case runs when any busybox was copied and calls it the image's; with the host's busybox the measurement is the host's.",
  acc=["at `fixed-at`, the case runs only with a busybox of verified provenance (PL-01) and is a counted SKIP otherwise: a host-busybox run reports it skipped (the stream's case)"],
  aw="Nothing on a device."),
 dict(id="PL-22", sev="Low", cat="Clarity", q="Q7", src="F-18", bug=True,
  title="last-good-scripts-test's own descriptions drift from its code: --help, the header's claims and recipes, the setsid advice",
  where=f"`{F}:239-250` (`--help`: *with the image's busybox*), `:7-148` (claims stop at `w`), `:162-226` (recipes stop at `v`), `:264`, `:266` (`setsid -f`)",
  what="`--help` promises the image's busybox (PL-01); the header claims sections `a` to `w` only and names recipes for `a` to `v`; the SIGINT advice names `setsid -f`, which avoids inheriting an ignored SIGINT only from a clean parent and cannot reset one.",
  acc=["at `fixed-at`, the header claims all 34 sections, names each section's positive (a recipe, a constructed case or none), and the help and the refusal message say what the code does: the diff quoted"],
  aw="Nothing on a device."),
 dict(id="PL-23", sev="Low", cat="Renovation", q="Q7", src="the § Q7 reading", bug=False,
  title="Rules and index rows describe this file wrongly or not at all",
  where="`upgrade-and-install.md:216-221`; `instruction-files.md:175` (Detail in `generic-x64-vm-testing.md`, which names the file twice and never describes it)",
  what="The rule says the test runs the image's busybox from the build root (true only where one is found); the index row points at a rule that never describes the file (T14's PL-12 shape).",
  acc=["the coordinator's lead (#1007's kind): no rule or index row is edited by this lane"],
  aw="Nothing written anywhere."),
 dict(id="PL-24", sev="Low", cat="Renovation", q="Q6", src="§ Q6's split proposal; the seat's Q5", bug=False,
  title="The file's split into subject files behind a shared harness",
  where=f"`{F}` (14,238 lines; `04` § Q6)",
  what="A split by subject (settings writers, backuptool, cloud scripts, network, the proxy, boot quirks) behind a shared harness library would make controls selectable and failures attributable; the cheaper half (PL-06) comes first.",
  acc=["the coordinator's lead: a design for the coordinator and the maintainer, recorded with its cost and gain in `04` § Q6"],
  aw="Nothing written anywhere."),
]
assert [x["id"] for x in I] == [f"PL-{i:02d}" for i in range(1, len(I)+1)]
def body(x):
    return (f"Found by the M6 T15 last-good-scripts-test audit (#662), {x['id']} ({x['src']}), "
            f"in `{A}/` on `feature/m6-tooling-last-good-test-662`. A test that passes without proving, or judges the wrong tools, is a defect (D-WORKFLOW-187); a stream will act on it.\n\n"
            f"## Code trace\n\n**Where (at `8ebaf8daad`):** {x['where']}\n\n**The defect:** {x['what']}\n\n"
            f"**What reading cannot prove:** recorded in `04` § Quality self-check and § Finding Verification.\n\n{VM}\n\n"
            "## Acceptance criteria\n\n" + "\n".join(f"- [ ] {a}" for a in x["acc"]) +
            f"\n\n**Already written:** {x['aw']}\n\nRefs #662\n")
out = ["# Punch list (Phases 5 and 6) — M6.P2 T15, the last-good scripts test (#662)\n",
       "Generated by `tools/t15-punch.py` from one list. 24 items: 0 Critical, 2 High, 13 Medium, 9 Low. Twenty-two carry a `bug` (filed at stage D); two are the coordinator's leads. F-08 was withdrawn after the seat's refutation (`04` § Second opinion).\n"]
for x in I:
    out.append(f"\n## {x['id']}: {x['title']}\n\n- **Severity:** {x['sev']}\n- **Category:** {x['cat']}\n- **Question:** {x['q']}\n- **Source:** {x['src']}\n- **Where:** {x['where']}\n- **What:** {x['what']}\n- **Acceptance:**\n" +
               "\n".join(f"  - {a}" for a in x["acc"]) + f"\n- **Already written:** {x['aw']}\n- **VM:** {VM}\n- **Tracked:** {'a `bug` filed at stage D' if x['bug'] else 'the coordinator (no bug)'}\n")
out.append("\n## Index\n\n```yaml\npunch_index:\n")
for x in I:
    out.append(f"- id: {x['id']}\n  severity: {x['sev']}\n  category: {x['cat']}\n  question: {x['q']}\n  source_finding: \"{x['src']}\"\n  tracked: \"{'bug (stage D)' if x['bug'] else 'the coordinator lead'}\"\n  outcome: \"open\"\n")
out.append("```\n\n## Phase 7 resolution gate\n\nPre-issue: every item is open until the coordinator's stage-E dispositions. Each row names what tracks it.\n\n| Item | Outcome | Tracked |\n| --- | --- | --- |\n")
for x in I:
    out.append(f"| {x['id']} | Open | {'a `bug` (stage D)' if x['bug'] else 'the coordinator lead'} |\n")
open(f"{A}/05-punch-list.md", "w").write("".join(out))
if "--bugs" in sys.argv:
    d = sys.argv[sys.argv.index("--bugs") + 1]; os.makedirs(d, exist_ok=True)
    for x in I:
        if x["bug"]:
            open(os.path.join(d, x["id"] + ".md"), "w").write(body(x))
            open(os.path.join(d, x["id"] + ".title"), "w").write("Bug: " + x["title"] + "\n")
sev = {}
for x in I: sev[x["sev"]] = sev.get(x["sev"], 0) + 1
print(len(I), "items", sev, "bugs", sum(1 for x in I if x["bug"]))
