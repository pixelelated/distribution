# vm-qa on 1a02664844

started 2026-10-11 19:56 UTC, guest a at :10022, cloud webdav (port 9010, hash=none modtime=no commit=partial bucket=no), image /workspace/artifacts/pixelelated-candidates/sha256/bd85b1b42f0170d7d82555af09cbe18762d6fc7eae63293bd0a8043e652db548/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261011T194522Z.g1a0266484423-from-ROCKNIX.img.gz, display: GL through virgl on /dev/dri/renderD128

| suite | result | time | log |
| --- | --- | --- | --- |
| scripts | FAIL (1) | 518s | `scripts.log` |
| lifetime | PASS | 1s | `lifetime.log` |
| wrapper | PASS | 0s | `wrapper.log` |
| vocabulary | PASS | 0s | `vocabulary.log` |
| french | PASS | 0s | `french.log` |
| quoting | PASS | 0s | `quoting.log` |
| menumap | PASS | 0s | `menumap.log` |
| register | PASS | 2s | `register.log` |
| pair-identity | PASS | 1s | `pair-identity.log` |
| fresh | PASS | 0s | `fresh.log` |
| round-trip | PASS | 84s | `round-trip.log` |
| exit | PASS | 26s | `exit.log` |
| time-to-play | PASS | 69s | `time-to-play.log` |
| walks | PASS | 1010s | `walks.log` |
| frame-diff | PASS | 2s | `frame-diff.log` |

**FAILED** -- 1 suite(s) failed; see the logs beside this file.

finished 2026-10-11 20:24 UTC

## time to play -- 1a02664844 on webdav

2026-10-11 20:07 UTC, guest at :10022, cloud `webdav`, payload `full`, 1 repeat(s).

Host state: **vm-qa on serval, guest a**. SSH round trip 5 ms (the launch POST goes over it); one screendump 61 ms, which is the resolution of every frame-derived number below.

Seconds, as median / mean / max.

### UI to game, at rest

| from the press to | median / mean / max | n |
| --- | --- | --- |
| the screen leaving the carousel | 0.01 / 0.01 / 0.01 | 1 |
| the handover (a black screen) | 0.01 / 0.01 / 0.01 | 1 |
| RetroArch existing | 0.51 / 0.51 / 0.51 | 1 |
| **the game's first frame** | **0.77 / 0.77 / 0.77** | 1 |
| RetroArch drawing (200 CPU ticks, or 30 four seconds on) | 4.60 / 4.60 / 4.60 | 1 |

### The exit sync, on its own

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.16 / 0.16 / 0.16 | 1 |
| **the last-sync-exit stamp** | **1.45 / 1.45 / 1.45** | 1 |
| the card gone from the screen | 3.51 / 3.51 / 3.51 | 1 |

Outcomes: completed x1. Payload seeded 616 KiB (RetroArch rewrites the auto-state on exit, so what moves is a little less; the log's rclone line has the bytes).

### Game to game, with the exit sync in flight

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.16 / 0.16 / 0.16 | 1 |
| the relaunch sent | 0.16 / 0.16 / 0.16 | 1 |
| the question answered (STOP IT AND PLAY, D-CLOUD-130) | 1.35 / 1.35 / 1.35 | 1 |
| **the next game's first frame** | **1.01 / 1.01 / 1.01** | 1 |
| the exit sync's stamp | - | 1 |

What the launch did to the sync, from the stamp's token: `?` x1.


renderer: virgl (Mesa Intel(R) Graphics (ARL)). -- the guest's Mesa, from the launch log; display: GL through virgl on /dev/dri/renderD128
