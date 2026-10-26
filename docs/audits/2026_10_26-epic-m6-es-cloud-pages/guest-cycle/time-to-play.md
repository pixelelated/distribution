# time to play -- 069fc27044 on webdav

2026-10-26 10:20 UTC, guest at :10022, cloud `webdav`, payload `full`, 3 repeat(s).

Host state: **(not stated)**. SSH round trip 5 ms (the launch POST goes over it); one screendump 61 ms, which is the resolution of every frame-derived number below.

Seconds, as median / mean / max.

## UI to game, at rest

| from the press to | median / mean / max | n |
| --- | --- | --- |
| the screen leaving the carousel | 0.01 / 0.05 / 0.12 | 3 |
| the handover (a black screen) | 0.01 / 0.05 / 0.12 | 3 |
| RetroArch existing | 0.47 / 0.49 / 0.56 | 3 |
| **the game's first frame** | **0.56 / 0.63 / 0.78** | 3 |
| RetroArch drawing (200 CPU ticks, or 30 four seconds on) | 4.63 / 4.60 / 4.65 | 3 |

## The exit sync, on its own

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.15 / 0.16 / 0.16 | 3 |
| **the last-sync-exit stamp** | **1.58 / 1.62 / 1.71** | 3 |
| the card gone from the screen | 4.01 / 4.01 / 4.01 | 3 |

Outcomes: completed x3. Payload seeded 628 KiB (RetroArch rewrites the auto-state on exit, so what moves is a little less; the log's rclone line has the bytes).

## Game to game, with the exit sync in flight

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.15 / 0.15 / 0.15 | 3 |
| the relaunch sent | 0.16 / 0.16 / 0.16 | 3 |
| the question answered (STOP IT AND PLAY, D-CLOUD-130) | 1.34 / 1.33 / 1.34 | 3 |
| **the next game's first frame** | **1.01 / 1.01 / 1.01** | 3 |
| the exit sync's stamp | - | 3 |

What the launch did to the sync, from the stamp's token: `?` x3.

