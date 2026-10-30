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

## [Stage C] 19:39 UTC 2026-10-30 — the guest window (granted 19:24), START 19:28:13 to RETURN 19:39:23

- **The order:** the host file was read at 19:27:40, the minute before START. My scripted open-START check matched no M7 line, because M7 stamps its lines `+00:00`, not `Z`. Read by hand at 19:27:53: the last M7 runtime line was the 13:35:50 RETURN, so no M7 START was open. The scripted check was wrong, and I said so in the START post.
- **The guest:** `generic-x64-vm run --headless --daemonize` through a wrapper (`guest-cycle/helpers/qemu-wrap`) adding `restrict=on` to the user netdev (read back from `/proc/<pid>/cmdline`), sockets under `/workspace/tmp/m6-t34/guest/`. Two boots: 640x480 (pid 743737, 19:27:41 to 19:35:30), then 1280x800 (pid 797892, 19:35:30 to 19:38:58). The detached stop timer was PID 743756, set to fire at 20:02:42; it was stopped with its child by recorded PIDs, unfired.
- **The records:** the RETURN post on #681 (comment 6531938082) carries the readings; the frames and reads are in `guest-cycle/`. Every frame is `image`. Gap 14 px at 640 and 28 px at 1280; the dim's ratio 0.314; the strip's four frames and L-02's pair identical. L-01 not reproduced on the image (0 log lines; the catalog carries `haut/bas`); new lead L-25 (the tabbed page's bar carries no component prompt at 1280); G-02, G-06, G-07, G-08 and G-10 CANNOT with their reasons.
- **The disk:** retired after the RETURN, as `guest-cycle/retired.txt` records; the census `qemu 0, compilers 0, listeners 0`.

## [Stage C] 20:00 UTC 2026-10-30 — 03, 04, 05; the packet; the seat's probe; the refutation started

- **`05`** is written by `tools/t34-05.py` from one item table: 26 items (0 Critical, 0 High, 5 Medium, 21 Low), each Open at the Phase 7 gate before stage D. `question:` uses the brief's numbering. **`04`** has the brief's seven questions, the take-up table disposed, and the plan's seven under Renovation face; it names the owed proofs (the unit build, the sanitizer cases, the syntax check). **`03`** is the audit's retrospective.
- **The council runtime:** `npm install --offline --prefix tools/council` rc 0 (install scripts not run). `COUNCIL_ENV_FILE=/nonexistent tools/council/run verify-pins`: `OK`. `... test`: 39/39, 127/127 and 19/19 pass, 0 fail.
- **The packet** (`tools/t34-packet.py` -> `second-opinions/t34-packet.md` and `packet-manifest.json`): 544,752 bytes and 95 sources (21 files whole, the 59's cited ranges, `02` to `05`, the brief's § 4). Its scan: 0 forbidden, 0 secret-shaped lines, 108 credential-shaped words each classed by file:line, 0 a value. `gpt-brief.md` (the ask plus the packet): 547,488 bytes, sha256 `126879915217b088c0d8f08925ee95413e9a504955b66c4ada6ec4b4c4e91b27`, rescanned 0 and 0.
- **Keyed invoke 1 of 2, the probe:** 19:59:53 to 20:00:06Z, `READY unknown`. Served `openai/gpt-6-astra` by OpenAI, effort `max`; verification, effort and provider PASS; `council-facilitator@1.14.1-pixelelated.2`.
- **Keyed invoke 2 of 2, the refutation,** started at 20:00Z with `--per-attempt-timeout-ms 3600000 --total-timeout-ms 10800000`, logging to `/workspace/tmp/m6-t34/audit.log`.
  - **What watches it:** the harness background task `b28z2x9mz`, which delivers its end.
  - **Its silent mode:** a hung seat ends only at those timeouts.

## [Stage C] 20:23 UTC 2026-10-30 — the refutation returned; the findings verified; one held

- **Keyed invoke 2 of 2:** 20:00:16 to 20:17:16Z, attempt 1 of 4, `finish=stop`, 24,250 bytes of content, 35,726 reasoning tokens. Served `openai/gpt-6-astra` by OpenAI at `max`; verification, effort and provider PASS. The reply was scanned before it was read: 0 forbidden, 0 secret-shaped.
- **No more keyed invokes:** exactly two were allowed, and both ran. The seat's "Sections I need" list got no second packet.
- **The grades** are recorded in `04` § Second opinion: PL-05 and PL-24 refuted (proposed withdrawn); PL-04 lowered to Low; PL-07 and PL-18 raised to Medium; the rest confirmed, confirmed with narrowing, or cannot tell.
- **G-1 to G-16:** each read at its cited lines at the pin before it was carried (11 confirmed, 5 with narrowing). They are PL-27 to PL-42.
  - **G-7 corrects this audit:** the stage-B statement of the grid's `clear()` contract was wrong, and `02` is recomposed with the correction.
  - **The seat's `:205` correction** (`addWithLabel`) is applied. Checking it found a seventh formatter, `:358` `setSubTitle` through `getFileName`: L-26, PL-43.
- **G-3 (PL-27) is security-sensitive,** and this repository and tracker are public. Its details are kept out of every committed file and post. The reply is held at `/workspace/tmp/m6-t34/held/gpt-audit.md` (mode 600; sha256 `609c488c...`, which the committed receipt binds). The maintainer's decision on the channel is asked for at the pause.
- **`05` now holds 43 items** (0 Critical, 1 High, 15 Medium, 27 Low), each Open until stage D disposes it.
- **The pre-issue lint** (`stage-c/lint-pre-issue.txt`):
  - on the committed tree: rc 1, one failure, the missing reply (the lint hashes it against the receipt, `tools/lint-audit-artifacts:105-110`);
  - with the held reply copied in for the run and removed straight after: `PASS pre-issue artifacts (does not certify resolution)`, rc 0. The reply was not left in the tree (`git status` after).

## [Stage D] 20:25 UTC 2026-10-30 — the audit issue; the pause

- **The audit issue:** #1307, `Audit: M6 T34 EmulationStation's core components -- 43 findings (0 critical, 1 high)`. Labels `audit` and `punch-list`, milestone M6, a sub-issue of #681. Its 43 checkboxes are generated from `05`. `tools/box-check --issue 1307`: `43 open checkbox(es), 0 fail`, rc 0. PL-27's line names no mechanism.
- **The pause** is posted on #681. The lane waits for the coordinator's dispositions, the four register rows, the channel for PL-27, the bug list and the unit build's timing.
