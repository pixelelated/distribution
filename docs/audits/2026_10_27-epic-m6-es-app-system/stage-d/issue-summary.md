Punch list of the M6.P2 T33 audit: EmulationStation's system layer (#680).

- **What was read:** the 77 paths of brief § 2 at the pin `16dbac5211`: the game lists, collections, metadata and filters (46 upstream-carried, byte-identical to `rocknix/master`); the fork's 17 helper units (27 files); NetworkThread and the CMake list (4 fork-modified). The fork's files were read whole; the upstream ones at their leads' lines, by six asserted generators, and by a labelled subagent for the floor's 35 rows.
- **reviewed-at:** `27bd8499f1`; **reviewed-at-es:** `16dbac5211`.

**Independent depth:** one seat, two keyed calls and no others (`stage-c/keyed-calls.txt`).
- **GPT-6 Astra at `max`:** probe PASS; refutation PASS, served `openai/gpt-6-astra` by OpenAI; 47 items, all accepted (`stage-c/astra-grades.md`).
- **The packet:** 539,134 bytes. The three-way scan found no value (`second-opinions/packet-manifest.json`). 6,399 of 16,276 slice lines were sent, with the trimmed ranges named.

**The host proofs:** nine fixtures, each FAIL at the pin and PASS under the proposed fix (`stage-c/runs.txt`). The unit build ran every target, `tests/app-unit`'s five case files for the first time: `TOTAL: 239 test cases in 5 binaries`, 0 failed.

**One guest window,** 19:01:31 (START) to 19:15:07 UTC (RETURN; stopped by pidfile at 19:14:06) on 2026-10-27, on the M6 image (M7's composition over the pin):
- **L-05 reproduced:** a `gamelist.xml` written from outside ES lost its entry at the next clean exit; the control system's file was byte-identical.
- **L-28 reproduced:** the unknown trigger dropped with no word.
- **L-06 not reproduced:** a plain collection never takes its path.
- G-05, G-07 and G-09 `CANNOT`. The disk retired; qemu 0, compilers 0.

The folder: `docs/audits/2026_10_27-epic-m6-es-app-system/` on `feature/m6-es-app-system-680`.
