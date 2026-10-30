# T34 (#681) running log: EmulationStation's core components

- **Model:** Opus 5.5 (`claude-opus-5-5`), high effort, the T3 session (`m6-t3-emulators`).
- **reviewed-at:** distribution `dff4fbd61d` (the lane tip; the dispatch's merge `00d490e654`, the coordinator's `200a9a032d` merged), with the ES pin `16dbac5211eea7e70db7394372033be2be7df829` beside it.
- **Host file** `/workspace/tmp/m7-m6-host-coordination.txt`, read at 2026-10-30T09:54:55Z (49 lines). Its last entry (09:26) queues M7's TLS proof windows and says T34's window waits behind all of M7's. **Census** at 09:55:01 UTC: qemu 0, compilers 0.

## [Stage A] 09:56 UTC 2026-10-30 — the pointer's keys, the first commands, the membership block, the § 5 runs; stopped at the usage limit

- **The pointer's eleven keys** were read against the brief's § 10 table before any command. All are present, and none names T33 or carries a seeding-error phrase. Two slips, neither a predecessor naming:
  - The brief's § 9 placeholder grep prints **1** on the pointer, not the dispatch's 0. The one match is the pointer's own line 43, the check line itself, which carries the tip placeholder's literal word; its three other placeholders were filled at seeding, so that line's own grep prints 5.
  - The Register key's D-SYS-014 is a row in `## Open decisions`. The decided table's highest SYS row is D-SYS-013. The other eight areas match my reading of the table.
- **§ 1 first commands:** every line printed as expected (`stage-a/first-commands.txt`). T33's ES tip is now `f802c55c62c1` (the brief read `dd86d7ce20a5`).
- **§ 2 membership block:** extracted from the brief byte for byte and run twice. Every expected line printed: `mine: 80 paths.txt: 80 equal: True`, the five summary lines, the 25 claims, the four ES-CORE rows, `wc -l 21971`, `grep -c 21984`, 80 and 80, and the shortstat twice. The outputs are in `.qa-scratch/t34/` (gitignored), to be carried into `01`.
- **§ 5 runs block** (`stage-a/runs.txt`, every line with its rc and wall time; block rc 0 in 3 s). Every expectation matched, with one brief erratum: the in-source gates command prints **13** lines. That is exactly § 4 Q7's list, where `VideoPlayerComponent.{cpp,h}:1` is two lines; the comment's "twelve" is the miscount. All eight lane tips are empty inside the 80.
- **#681's body:** its 21 checkboxes equal the brief's § 7 byte for byte. Issue states are in `stage-a/issue-states.txt`.
- **The ES worktree** is at the pin, clean, with an empty diff against it. Nothing was written there.
- **The rules:** six rule files in T34's worktree differ from the copy this session loaded (the T3 worktree's): `device-builds`, `engineering-practices`, `es-code-traps`, `es-player-text`, `es-ui-style-guide`, `generic-x64-vm-testing`. T34's are the ones the brief cites, and they are read from this worktree.
- **Stopped** here at the session's usage limit.
  - **Stage A still owes:** `01-research-notes.md` § Scope, the pointer's checkpoint (and its line-43 check rewritten), and the day's work-log entry headed #681.

## [Stage A] 14:24 UTC 2026-10-30 — resumed after the usage-limit stop; the stage-A close

- **The stop:** from just after `22c0d5a2c2` (about 09:57) to 14:22 UTC, the session's usage limit. Nothing of T34 ran in the gap: no process, and the ES worktree at the pin, clean.
- **The host file, read at 2026-10-30T14:24:16Z (59 lines):** M7's TLS native window ran 13:25:28 to 13:26:11, and its TLS VM window 13:33:45 to 13:35:50 (the guest's certificate generation failed; nothing remains). At 14:21 the coordinator granted M7 a follow-up TLS guest, with T34's window asked for after stage B and after every M7 window. **Census** at 14:24:16: qemu 0, compilers 0.
- **The placeholder check, corrected:** the commit `22c0d5a2c2` carried this file with two of the brief's placeholder words spelled out, so the brief's § 9 grep printed 1 on it; I had committed without gating on that line. Both are reworded. `stage-a/runs.txt` and `01` quote the brief's removal-check comment, so the four words are written hyphenated there (said in `runs.txt`'s first line). The grep now prints 0 on `00`, `01`, every `stage-a/` file and the pointer.
- **Written:**
  - `01-research-notes.md` (§ Scope, generated from `stage-a/membership-block.txt`; § The § 5 runs at stage A, from `stage-a/runs.txt`; § Read this session);
  - `stage-a/membership-block.txt` and `stage-a/paths.txt`;
  - the pointer (the stage-A focus, its line 43 rewritten, the first checkpoint line);
  - the day's work-log entry headed #681.

## [Stage B] 14:46 UTC 2026-10-30 — 02 composed; the window plan; the request

- **`02-forward-audit.md`** is composed by `tools/t34-02.py` from `tools/t34-02.template.md` and nine generators (coverage, leads, layouts, constants, input, lifetimes, reads, words, includes). Each was seen to exit 1 on a constructed drift (`stage-b/generator-drifts.txt`). It has 510 lines, its 16 sections in the brief's § 6 order, and 80 coverage rows by § 7's own command; the placeholder grep reads 0.
- **New leads:**
  - L-22: the card's `close()` writes its closing state unlocked from the holders' threads while `update()` reads it;
  - L-23: `"add star"` is outside `_()`;
  - L-24: a video component's BACK prompt is labelled SELECT.
- **Readings:** L-09 is sound at the pin, by the writer's erase. § 1 (g)'s `setOpacity` is unreachable on the fork's images. `UntintedImageComponent` is at `GuiMenu.cpp:6401`.
- **The window plan** is `stage-b/window-plan.md`: 1,410 s by the brief's command re-run; 30 + 5 minutes; two boots.
- **The push route:** HTTPS with `gh`'s credential (the friction lines).
