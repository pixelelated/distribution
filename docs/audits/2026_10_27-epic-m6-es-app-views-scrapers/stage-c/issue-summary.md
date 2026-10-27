Punch list of the M6.P2 T32 audit: EmulationStation's game list views, scrapers and services (#679).

- **What was read:** the 42 paths under `es-app/src/views/`, `views/gamelist/`, `scrapers/` and `services/`, at the pin `16dbac5211`. The six fork-modified files were read whole. The 36 upstream ones, byte-identical to `rocknix/master`, were read at their leads' lines and by seven generators. `httplib.h` was read by fingerprint and at its request path.
- **reviewed-at:** `603b358a14`; **reviewed-at-es:** `16dbac5211`.

**Independent depth:** one seat, two keyed calls and no others (`stage-c/keyed-calls.txt`).
- **GPT-6 Astra at `max`:** probe PASS; refutation SEAT_RESULT (`stage-c/astra-grades.md`).
- **The packet:** 433,943 bytes. The three-way scan found no value (`second-opinions/packet-manifest.json`). 6,240 of 17,311 slice lines were sent, with the trimmed ranges named.

**One guest window,** 16:08:36 to 16:22:34 UTC on 2026-10-27, on the M6 image (M7's composition over the pin):
- 3.13 and 3.19 shown on the image: offline, COMPLETED, GAMES SCRAPED: 9 for ten games;
- L-08 shown with its control;
- G-07 and G-10 `CANNOT` (`02` § The guest cycle).

**Seven host harnesses** fail at the pin and pass their controls (`stage-c/runs.txt`). Three of the failures are memory errors in the shipped build's shape: two SEGVs and a use-after-free. **The floor's 27** were read at their lines (`stage-c/floor.md`).

- **The folder:** `docs/audits/2026_10_27-epic-m6-es-app-views-scrapers/` on `feature/m6-es-app-views-scrapers-679` at `HEADCOMMIT`.
- **The list:** `05-punch-list.md`. `tools/lint-audit-artifacts --phase pre-issue`: `PASS pre-issue artifacts (does not certify resolution)`.
