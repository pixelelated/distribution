# Running log — M6.P2 T26, EmulationStation's main menu, GuiMenu (#673)

- **Executor:** Opus 5.5 at high effort, the session `m6-t5-build-engine` (the dispatch comment on #673, 02:35 UTC on 2026-10-27; its header reads 2026-10-26, a slip of the date).
- **Depth:** Independent -- one seat, GPT-6 Astra at `max`: a probe and one refutation, exactly two keyed invokes.
- **The brief:** `docs/reviews/briefs/es-guimenu.md` at `4b0ee281b5` (version 2), byte-equal to the tree's copy (`git diff --quiet 4b0ee281b5 HEAD -- <brief>`).
- **reviewed-at:** `db7be4b104`, the distribution worktree's HEAD at dispatch, the lane tip the dispatch names.
- **reviewed-at-es:** the pin `16dbac5211eea7e70db7394372033be2be7df829`. The ES worktree `feature/m6-es-guimenu-673` is at the pin and clean.
- **Can this be done on the VM?** Yes. The host goes first: every read, count and table, and the ten Python harnesses that extract this file's functions and compile them with the host's `g++`. Then one guest window, asked for on #673 at stage B's end and granted in the shared log's queue. Nothing runs on a handheld or against the owner's accounts.
- **The rules followed:** this worktree's `.claude`, `CLAUDE.md` and `AGENTS.md` differ from local `next` because they carry the coordinator's branch, newer than `next` (`git diff --stat origin/next -- .claude`: nine files, 194 insertions). Its additions to `engineering-practices.md` and `es-code-traps.md` were read at stage A:
  - a count, a line number or a hash is produced by a command at the hash it is about, and **a total is the tool's line, never a sum made in the head** (T21's lesson, now this rule);
  - `rc=$?` goes on its own line;
  - a granted window names what stops the guest at its bound;
  - a stub is checked against the unfixed code before its FAIL is recorded;
  - a stream's non-ASCII grep judges the lines it added;
  - curl's header callback is read by its length.

  `generic-x64-vm-testing.md`'s additions are read at stage B, for the window.

## [Stage A] 02:36 to 02:50 UTC — the first commands, the block, the parser, the runs, the context

- **The host at dispatch** (`stage-a/census.txt`, 02:39:38 UTC): qemu live 0, compilers 0. `/tmp/m7-m6-host-coordination-20261023.txt` ends with M7's RETURN `prose-ui01` (00:16:27 UTC) and the coordinator's acknowledgement at 00:16 UTC. No guest runs from this lane before a grant on #673.
- **The first commands (§ 1),** all as the brief expects: the worktree clean (0), stacked on `8ebaf8daad`, no change under `packages` or `projects` since it, `651150fc88` present locally; the ES worktree at the pin, 0 changes, merge base `bccd715707`; T18's punch list reachable (23 items); `register-check` passing.
- **The membership block (§ 2),** every figure as the brief states (`stage-a/membership.txt`): `selects 1 paths 2 lines 11883`, both shipped and fork-own; `wc -l` 11883; both paths in the merge base; numstat 5124/436 and 23/1.
- **The definitions parser** (`tools/t26-defs.py`, its rules in its docstring): 156 definitions at the pin (63 members, 92 statics, 1 free -- `getCountryCodes` classed static), 60 at the base; 97 added, 1 removed (`openWifiSettings`), of 59 in common 12 changed and 47 unchanged by exact text (10 and 49 with whitespace removed); the ten longest as the brief lists them (`stage-a/defs.txt`, one line per definition). Its first run refused a raw string literal at `:1859` (`R"(/usr/bin/timeinfo current_timezone)"`); the parser now blanks raw strings.
- **The runs (§ 5)** (`stage-a/runs.sh`, its output `stage-a/runs.txt`, each with exit and wall time): every figure as the brief expects, among them:
  - 17 lines with `cloudSetupPresent(`, the definition at `:6484` among them;
  - 12 uncached reads; `qrPath` and `isRegularFile` at `:4136`, `:7767`, `:7769`, `:7792`, `:7793`; the "uncached" comment at `:4154-4156`;
  - the ten harnesses, each rc 0, each last line as the brief prints it;
  - `55 screen(s) at 16dbac521, 31 in the map, 24 declared unmapped, 0 missing`;
  - `es-untranslated: 706 fork string(s) in the source, 706 with French, 0 without`;
  - 0 non-ASCII comment lines (rc 1); `es-syntax-check` exit 2 with no build root; `g++`'s first error at `InputConfig.h` (SDL);
  - the nine builder greps (35, 6, 15, 5, 169, 99, 129, 90, 16; 564 in all by the brief's own count);
  - 86 `#if` lines, 109 `new GuiMsgBox`; 1447 lines with `_("`, 980 unique one-line literals, 978 with French (`tools/t26-french.py`), the two without upstream's fuel-gauge rows;
  - 9 upstream commits since the base, +155/-12, `cada856d8` among them (3 insertions, 10 deletions in this file);
  - the removal check empty.
- **Not run at stage A:** `t26-rows.py` and `t26-structure.py`, the generators of `02` § The rows and the structure tables, are stage B's; their runs-block lines are run there.
- **Read at stage A** (`01` § Context): the brief whole with its version note; the dispatch comment and its errata; #673's two routed notes (T18's of 11:13 UTC on 2026-10-26, T21's of 00:31 UTC); T20's `02` § What T21 and T26 inherit; sixteen register rows; nine blindspots; the menu map's headings and `:403-408` and `:664-669`; the 27 issues by title and state; the history and the callers (`stage-a/history-callers.txt`).
- **Nothing else ran:** no image build, no fetch of a source (one `git fetch origin next`, a read of our own remote, to compare the rules), no guest, no handheld, no council call.

## [Stage B] 02:52 to 08:04 UTC — the generators, the reading, 02, the window plan

- **Five generators under `tools/`**, each with its method in its docstring, its counts asserted and exit 1 on drift, and each seen to exit 1 on a constructed drift (`stage-b/runs.txt`, the four `neg-*.txt`): `t26-rows.py` (561 calls, 275 value-binding rows, 267 writes), `t26-pages.py` (60 pages, 65 titles, 159 runs of which 131 on the interface thread and 116 of those unbounded, 108 dialogs), `t26-structure.py` (16 + 10 transitions, 37 reads with 12 uncached, 74 duplicated labels, 86 regions, 869 lines no ROCKNIX image compiles), `t26-merge.py` (9 upstream commits, 15 hunks, 8 meeting the fork's 148), and `t26-defs.py` from stage A. `t26-assemble-02.py` builds `02-forward-audit.md` from `stage-b/02-template.md` and the generators' tables, run at the pin's bytes.
- **The generators were corrected as they were read, not after** -- each correction found by reading the lines a figure stood on: the first asserted counts were placeholders until the method held; a change callback's receiver, an if/else pair building one row, a local standing for its component and a capture list counted as a mention each moved the rows' assignment; the reader's `global.` fallback (`001-functions:164-172`) turned 6 "unread" keys into read ones; a helper's own `timeout` and its own worker moved the pages' bound and thread columns; a page builder that runs a process is an opener, not a run; "build time" became "outside every save hook" once `:6699` was read as a press.
- **The reading** (`stage-b/reading-notes.md`): the 97 added definitions and the fork's three classes whole; the changed and unchanged definitions at the leads' lines; the neighbours each lead turns on (`GuiSettings`, `GuiMsgBox`, `FileSystemUtil`, `Platform`, `TextureResource`, `ImageComponent`, `SwitchComponent`, `ComponentList`, `StringUtil`, `CloudText`; `cloud_remote`, `cloud_oauth`, `setrootpass`, `001-functions`, `setsettings.sh` at `8ebaf8daad`); T21's `GuiSettings.cpp` at `3ae9610b0` by `git show`.
- **One fixture** (`stage-b/positives/getshoutput.cpp`, `Platform.cpp:891-905` verbatim, run under bubblewrap `--clearenv`): L-05's four cases.
- **`02`:** 30 leads. New against the brief: L-02 (a QR texture asked for by path), L-18 (`:8460` names a row `c8dc72cf9` renamed), L-19 (the match's English refusal), L-20 (`:8116`'s runtime msgid). Corrections to the brief: MANUAL UPDATES is the fork's (`975235429`); `led.colour`, `:2989` and `:3209` are under `BATOCERA` (never built); the six unguarded credential rows are fixed by T21's S1 in `GuiSettings` (#1185); 11 of the brief's 33 unread keys hold once the global fallback is read.
- **The window plan** (`stage-b/window-plan.md`): twelve steps, 45 minutes plus 5 of grace, stopped by pidfile at the bound, image versus tree first.
- **Nothing else ran:** no image build, no fetch, no guest, no handheld, no council call.

## [Window] 08:06 to 08:31 UTC — the guest, granted on #673

- **Granted** 08:06 UTC (comment 6436803989). The guarded swap reclaim ran once before the guest (`READY`, 8,191 MB to 0). **START** 08:08:16 UTC, **RETURN** 08:31:02 UTC, each with its census on #673 and in the shared host file; the guest stopped 08:30:06 by `tools/vm-stop` on its pidfile (rc 0), 22 minutes into the 45.
- **Proved on the image** (M7's composition over the pin, by its two literals): L-01 with its control, L-09, L-10, L-18 (EN and FR), L-20. **Not reached:** L-02 (`ON_DEVICE=yes`), L-16 at 640x480 (full-screen menus). **Read:** L-11's seed already carries the threshold; L-13's reach (two rows hidden, two reachable).
- **The disk retired:** `t26.qcow2`, 2,310,275,072 bytes, sha256 `f9fec3fb…c81e`, removed; the leftover check clean (`guest-cycle/retired.txt`).
- **Mine:** a malformed `vm-serial sh` call left the guest's shell in `cat` (cleared with Ctrl-C and Ctrl-D); `vm-stop`'s first call refused a timeout above 60 s; two key bursts overshot. None reached a result.
- **Nothing else ran:** no image build, no fetch, no handheld, no account, no council call.

## [Stage C] 08:31 UTC onward — 03 and 04, the packet, the seat

- **A correction:** commit `31d55a8a7e`'s message says "38 frames"; `ls guest-cycle/frames | wc -l` reads 50. A hand count, against the rule that a total is the tool's line.
- **03 and 04** written before the seat saw the packet.
- **The packet** (`stage-c/packet.py`, T21's builder adapted): 92 sections, 563,026 bytes; the secret scan proven to fire on a run-time fake line and silent on the packet; the forbidden-terms check run on all 91 sections, 0 hits; 24 credential-shape hits read at their lines and dispositioned by name (code names, a loop counter, prose, a masked public URL), none a value; `GuiMenu.cpp` 6,305 of 11,747 lines in 46 excerpts, the 47 trimmed ranges named in `second-opinions/packet-manifest.json`.
- **The council runtime:** `npm install --offline` in `tools/council` (the dispatch's allowance); every other council call keyless (`COUNCIL_ENV_FILE=/nonexistent`: `invoke --help`, `efforts`).
- **Keyed call 1 of 2** (`stage-c/keyed-calls.txt`): the probe, 08:39:25 to 08:39:37 UTC, rc 0; served `openai/gpt-6-astra`, provider OpenAI, effort `max`, identity, effort and provider verification each PASS, `council-facilitator@1.14.1-pixelelated.2`.
- **Keyed call 2 of 2:** the refutation over the packet, started 08:40 UTC.
