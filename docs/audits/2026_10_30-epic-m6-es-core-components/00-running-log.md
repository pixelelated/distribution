# T34 (#681) running log: EmulationStation's core components

- **Model:** Opus 5.5 (`claude-opus-5-5`), high effort, the T3 session (`m6-t3-emulators`).
- **reviewed-at:** distribution `dff4fbd61d` (the lane tip; MERGE_HASH `00d490e654`, the coordinator's `200a9a032d` merged), with the ES pin `16dbac5211eea7e70db7394372033be2be7df829` beside it.
- **Host file** `/workspace/tmp/m7-m6-host-coordination.txt`, read at 2026-10-30T09:54:55Z (49 lines). Its last entry (09:26) queues M7's TLS proof windows and says T34's window waits behind all of M7's. **Census** at 09:55:01 UTC: qemu 0, compilers 0.

## [Stage A] 09:56 UTC 2026-10-30 — the pointer's keys, the first commands, the membership block, the § 5 runs; stopped at the usage limit

- **The pointer's eleven keys** were read against the brief's § 10 table before any command. All are present, and none names T33 or carries a seeding-error phrase. Two slips, neither a predecessor naming:
  - The brief's § 9 placeholder grep prints **1** on the pointer, not the dispatch's 0. The one match is the pointer's own line 43, the check line itself, which carries the literal TIPHASH; its three other placeholders were filled at seeding, so that line's own grep prints 5.
  - The Register key's D-SYS-014 is a row in `## Open decisions`. The decided table's highest SYS row is D-SYS-013. The other eight areas match my reading of the table.
- **§ 1 first commands:** every line printed as expected (`stage-a/first-commands.txt`). T33's ES tip is now `f802c55c62c1` (the brief read `dd86d7ce20a5`).
- **§ 2 membership block:** extracted from the brief byte for byte and run twice. Every expected line printed: `mine: 80 paths.txt: 80 equal: True`, the five summary lines, the 25 claims, the four ES-CORE rows, `wc -l 21971`, `grep -c 21984`, 80 and 80, and the shortstat twice. The outputs are in `.qa-scratch/t34/` (gitignored), to be carried into `01`.
- **§ 5 runs block** (`stage-a/runs.txt`, every line with its rc and wall time; block rc 0 in 3 s). Every expectation matched, with one brief erratum: the in-source gates command prints **13** lines. That is exactly § 4 Q7's list, where `VideoPlayerComponent.{cpp,h}:1` is two lines; the comment's "twelve" is the miscount. All eight lane tips are empty inside the 80.
- **#681's body:** its 21 checkboxes equal the brief's § 7 byte for byte. Issue states are in `stage-a/issue-states.txt`.
- **The ES worktree** is at the pin, clean, with an empty diff against it. Nothing was written there.
- **The rules:** six rule files in T34's worktree differ from the copy this session loaded (the T3 worktree's): `device-builds`, `engineering-practices`, `es-code-traps`, `es-player-text`, `es-ui-style-guide`, `generic-x64-vm-testing`. T34's are the ones the brief cites, and they are read from this worktree.
- **Stopped** here at the session's usage limit.
  - **Stage A still owes:** `01-research-notes.md` § Scope, the pointer's checkpoint (and its line-43 check rewritten), and the day's work-log entry headed #681.
