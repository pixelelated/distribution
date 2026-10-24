# vm-qa on 069fc27044

started 2026-10-24 19:25 UTC, guest a at :10022, cloud webdav (port 19010, hash=none modtime=no commit=partial bucket=no), image (already up), display: GL through virgl on /dev/dri/renderD128

| suite | result | time | log |
| --- | --- | --- | --- |
| fresh | PASS | 1s | `fresh.log` |
| round-trip | PASS | 84s | `round-trip.log` |
| exit | PASS | 27s | `exit.log` |
| time-to-play | PASS | 72s | `time-to-play.log` |
| frame-diff | SKIP | 0s | `frame-diff.log` |

**PASSED with 1 suite(s) SKIPPED** -- a skipped suite could not run (its log says why) and has not passed.

finished 2026-10-24 19:28 UTC

## time to play -- 069fc27044 on webdav

2026-10-24 19:28 UTC, guest at :10022, cloud `webdav`, payload `full`, 1 repeat(s).

Host state: **vm-qa on serval, guest a**. SSH round trip 6 ms (the launch POST goes over it); one screendump 62 ms, which is the resolution of every frame-derived number below.

Seconds, as median / mean / max.

### UI to game, at rest

| from the press to | median / mean / max | n |
| --- | --- | --- |
| the screen leaving the carousel | 0.10 / 0.10 / 0.10 | 1 |
| the handover (a black screen) | 0.10 / 0.10 / 0.10 | 1 |
| RetroArch existing | 0.56 / 0.56 / 0.56 | 1 |
| **the game's first frame** | **0.74 / 0.74 / 0.74** | 1 |
| RetroArch drawing (200 CPU ticks, or 30 four seconds on) | 4.64 / 4.64 / 4.64 | 1 |

### The exit sync, on its own

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.15 / 0.15 / 0.15 | 1 |
| **the last-sync-exit stamp** | **1.59 / 1.59 / 1.59** | 1 |
| the card gone from the screen | 3.51 / 3.51 / 3.51 | 1 |

Outcomes: completed x1. Payload seeded 616 KiB (RetroArch rewrites the auto-state on exit, so what moves is a little less; the log's rclone line has the bytes).

### Game to game, with the exit sync in flight

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.15 / 0.15 / 0.15 | 1 |
| the relaunch sent | 0.16 / 0.16 / 0.16 | 1 |
| the question answered (STOP IT AND PLAY, D-CLOUD-130) | 1.37 / 1.37 / 1.37 | 1 |
| **the next game's first frame** | **1.01 / 1.01 / 1.01** | 1 |
| the exit sync's stamp | - | 1 |

What the launch did to the sync, from the stamp's token: `?` x1.


renderer: virgl (Mesa Intel(R) Graphics (ARL)). -- the guest's Mesa, from the launch log; display: GL through virgl on /dev/dri/renderD128
