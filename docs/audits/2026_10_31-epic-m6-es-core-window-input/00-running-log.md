# Running log — M6.P2 T35, EmulationStation's window, input, settings and the rest of es-core (#682)

- **Model:** Opus 5.5 (`claude-opus-5-5`), **effort high**. The session is the T5 session (`m6-t5-build-engine`), free since T33's close-out.
- **reviewed-at:** `b1f2908a55`, the distribution worktree's HEAD at stage A: the coordinator's `be119338ff` merged at `b51dd8a805`, then the pointer seeded. **reviewed-at-es:** the pin `16dbac5211eea7e70db7394372033be2be7df829`. The ES worktree `feature/m6-es-core-window-input-682` is at the pin and clean.
- **The dispatch:** #682 comment 6539807425, 05:56:41 UTC 2026-10-31. It names the brief `docs/reviews/briefs/es-core-window-input.md` at `8b5d9b9b62` (version 2), the lane tip `b1f2908a55`, and a census at 05:56 of qemu 0 and compilers 0.
- **The host,** read at 06:00:08Z (`stage-a/host.out`):
  - M7 holds a native window grant (the coordinator's 05:42 line) and its no-NIC guest next.
  - T34's lane wrote `stage E S2 compiles START` at 05:55:03Z, with no END line at the read.
  - The census at 06:00:08Z: qemu 0, compilers 0 (cc1plus), g++ 0.
- **Can this be done on the VM?** Yes. The host goes first, then one guest window granted on #682 (brief § 5 item 1).
- **The pointer's eleven keys,** read against the brief's § 10 table before the first command after `cat`: none names T34 (`es-core-components`, the 80 paths or the T3 session). Each reads the value § 10 asks for. One note, not a predecessor error: the `Branch (distribution):` line says the lane's own tip is `b51dd8a805`, while HEAD is `b1f2908a55`, the pointer's own seeding commit, which the dispatch names.
- **The rules followed:**
  - This worktree's `.claude`, `CLAUDE.md` and `AGENTS.md` differ from local `next` (`8ebaf8daad`) by 11 files (+211/-11). They carry the coordinator's branch, which is newer than `next`.
  - The session's rules were loaded at start from the T5 worktree (`m6-build-engine-652`). Six of this worktree's rule files are newer than those: `device-builds`, `engineering-practices`, `es-code-traps`, `es-player-text`, `es-ui-style-guide` and `generic-x64-vm-testing` (`git diff --stat feature/m6-build-engine-652 HEAD -- .claude CLAUDE.md AGENTS.md`: 8 files, +174/-9, two of them skill files). Their hunks were read from this worktree before this log was written, so where a rule matters here, this worktree's copy is the one read.

## [Stage A] 05:57 to 06:03 UTC 2026-10-31 — the brief, the first commands, the block, the runs

- **Read:** the dispatch comment whole; the pointer (`cat`); the brief at `8b5d9b9b62`, 2,120 lines (the worktree copy equals that commit's), § 10 first and then § 1 to § 9; the six newer rule hunks above (`git diff feature/m6-build-engine-652 HEAD -- .claude/rules`).
- **The first commands** (brief § 1; `stage-a/first-commands.out`, 05:58:44Z): every line prints as § 1 expects -- `stacked`, `upstream-next-is-here`, the ES worktree at the pin with 0 status lines, `cada856d86`, `f6c542872e`, `b2ceb55a7e`, `1750dded8c`, `register-ok`, `stacked-on-P1`, `coordinator-tip-merged`, the diffs against `8ebaf8daad` and `b51dd8a805` empty, `inventory`, and § 9's placeholder grep on the pointer `0`.
  - **One delta:** T34's `origin/feature/m6-es-core-components-681` now resolves, to `dbe4c2db0f`, where the brief expected a `fatal:` line. Its delta inside the 96 is empty (the § 5 run below). Recorded, not a stop.
- **The membership block** (brief § 2, run verbatim from the brief's text; `stage-a/membership.sh`, `.out`; 05:58:56Z to 05:58:57Z, rc 0):
  - `96 .qa-scratch/t35/paths.txt`;
  - `mine: 96 paths.txt: 96 equal: True`;
  - `lines: 22575 reach: {'shipped': 96} tier: {'fork-own': 13, 'upstream-carried': 83} lang: {'cmake': 1, 'c-header': 51, 'c++': 44}`;
  - `fork-own lines: 6759`; `read lines: 22575`; `wc -l 22567`; `grep -c 22575`; `95` and `95`;
  - `13 files changed, 247 insertions(+), 71 deletions(-)` twice.

  Every line is § 2's, byte for byte. **One record-only delta:** the brief's prose lists two `GuiLoading.h` rows under `CLAIMS` that the script's own `named` list does not carry, so the block prints 30 claims, not 32. The four `ES-CORE BY SLICE` rows are § 1's.
- **The § 5 runs** (`stage-a/runs.sh`, `.out`; 05:59:32Z to 05:59:35Z): 22 runs, each wrapped in its own `rc=$?` line and a `date +%s` pair around the brief's lines, unchanged inside. Every figure prints as expected, with these deltas recorded beside the expectations:
  - T34's ref prints an empty stat inside the 96, not `fatal:`.
  - The lock grep prints `66 78 94 143 181 196`. The brief's comment expects `181` and `196`; the other four are the acquisitions in `RegisterComponent`, `UnregisterComponent`, `ResetComponent` and the destructor, as § 2's table names them.
  - The `say(` grep prints `44 234 240`, three lines, as correction 7 and L-16 state, though the comment names two.
  - The gates run prints one line of 128 items (counted, `run rc=0`). The `ROCKNIX` grep its expectation names is added as a run of its own: 3 lines, `InputManager.cpp:585 Paths.cpp:76 Splash.h:10`.
  - The three STAGE C commands are `CANNOT` at stage A: their scripts are the lane's stage-C inputs.
  - The removal check, with the lane's own tip `b51dd8a805` filling the brief's placeholder, prints empty for both diffs. The run of the literal placeholder word was dropped from the record so § 9's placeholder grep reads 0 on every artifact.
- **The issue states** (brief § 3 item 9; `stage-a/issues.out`, read at 06:00:08Z):
  - **OPEN `bug`:** #1283, #1276, #1212, #1178, #1305, #1195, #1245.
  - **OPEN, no label:** #682 (1 comment, the dispatch), #1192, #54, #1137, #1138, #1141, #585, #63, #65, #680, #681.
  - **OPEN, labelled:** #1307 (`audit`, `punch-list`) and #700 (`epic`).
  - **CLOSED:** #1270, #115, #149, #177, #178, #246, #283, #299, #48.
- **Nothing was written in the ES worktree.** Its HEAD is the pin, with 0 status lines (the first commands, and the removal check's second diff). No guest, no image build, no fetch and no keyed call. The scratch is `/workspace/tmp/m6-t35/tmp`, made after `df -i` (26% of the inodes used).
