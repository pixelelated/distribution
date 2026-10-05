# vm-qa on d6e8390c93

started 2026-10-05 20:29 UTC, guest d at :10026, cloud webdav (port 9040, hash=none modtime=no commit=partial bucket=no), image (already up), display: software rendering (no GL display)

| suite | result | time | log |
| --- | --- | --- | --- |
| exit | PASS | 26s | `exit.log` |
| time-to-play | PASS | 85s | `time-to-play.log` |

**PASSED** -- every suite that ran passed.

finished 2026-10-05 20:31 UTC

## time to play -- d6e8390c93 on webdav

2026-10-05 20:30 UTC, guest at :10026, cloud `webdav`, payload `full`, 1 repeat(s).

Host state: **vm-qa on serval, guest d**. SSH round trip 4 ms (the launch POST goes over it); one screendump 202 ms, which is the resolution of every frame-derived number below.

Seconds, as median / mean / max.

### UI to game, at rest

| from the press to | median / mean / max | n |
| --- | --- | --- |
| the screen leaving the carousel | 0.22 / 0.22 / 0.22 | 1 |
| the handover (a black screen) | 0.22 / 0.22 / 0.22 | 1 |
| RetroArch existing | 0.46 / 0.46 / 0.46 | 1 |
| **the game's first frame** | **0.64 / 0.64 / 0.64** | 1 |
| RetroArch drawing (200 CPU ticks, or 30 four seconds on) | 4.55 / 4.55 / 4.55 | 1 |

### The exit sync, on its own

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.15 / 0.15 / 0.15 | 1 |
| **the last-sync-exit stamp** | **1.67 / 1.67 / 1.67** | 1 |
| the card gone from the screen | - | 1 |

Outcomes: completed x1. Payload seeded 616 KiB (RetroArch rewrites the auto-state on exit, so what moves is a little less; the log's rclone line has the bytes).

### Game to game, with the exit sync in flight

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.15 / 0.15 / 0.15 | 1 |
| the relaunch sent | 0.16 / 0.16 / 0.16 | 1 |
| the question answered (STOP IT AND PLAY, D-CLOUD-130) | 0.97 / 0.97 / 0.97 | 1 |
| **the next game's first frame** | **1.01 / 1.01 / 1.01** | 1 |
| the exit sync's stamp | - | 1 |

What the launch did to the sync, from the stamp's token: `?` x1.


renderer: llvmpipe (LLVM 22.1.8, 256 bits). -- the guest's Mesa, from the launch log; display: software rendering (no GL display)
