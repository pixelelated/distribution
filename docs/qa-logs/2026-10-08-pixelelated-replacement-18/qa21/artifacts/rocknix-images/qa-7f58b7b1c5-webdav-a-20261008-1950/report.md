# vm-qa on 7f58b7b1c5

started 2026-10-08 19:50 UTC, guest a at :10022, cloud webdav (port 9010, hash=none modtime=no commit=partial bucket=no), image /workspace/artifacts/pixelelated-candidates/sha256/f557176651026f59bb5931993b12491a6019c0383321fb89fa1a05a596514fe6/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz, display: GL through virgl on /dev/dri/renderD128

| suite | result | time | log |
| --- | --- | --- | --- |
| scripts | PASS | 500s | `scripts.log` |
| lifetime | PASS | 1s | `lifetime.log` |
| wrapper | PASS | 0s | `wrapper.log` |
| vocabulary | PASS | 0s | `vocabulary.log` |
| french | PASS | 0s | `french.log` |
| quoting | PASS | 0s | `quoting.log` |
| menumap | PASS | 0s | `menumap.log` |
| register | PASS | 2s | `register.log` |
| pair-identity | PASS | 1s | `pair-identity.log` |
| fresh | PASS | 0s | `fresh.log` |
| round-trip | PASS | 86s | `round-trip.log` |
| exit | PASS | 27s | `exit.log` |
| time-to-play | PASS | 69s | `time-to-play.log` |
| walks | PASS | 1009s | `walks.log` |
| frame-diff | FAIL (1) | 2s | `frame-diff.log` |

**FAILED** -- 1 suite(s) failed; see the logs beside this file.

finished 2026-10-08 20:19 UTC

## time to play -- 7f58b7b1c5 on webdav

2026-10-08 20:01 UTC, guest at :10022, cloud `webdav`, payload `full`, 1 repeat(s).

Host state: **vm-qa on serval, guest a**. SSH round trip 5 ms (the launch POST goes over it); one screendump 66 ms, which is the resolution of every frame-derived number below.

Seconds, as median / mean / max.

### UI to game, at rest

| from the press to | median / mean / max | n |
| --- | --- | --- |
| the screen leaving the carousel | 0.10 / 0.10 / 0.10 | 1 |
| the handover (a black screen) | 0.10 / 0.10 / 0.10 | 1 |
| RetroArch existing | 0.50 / 0.50 / 0.50 | 1 |
| **the game's first frame** | **0.69 / 0.69 / 0.69** | 1 |
| RetroArch drawing (200 CPU ticks, or 30 four seconds on) | 4.55 / 4.55 / 4.55 | 1 |

### The exit sync, on its own

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.15 / 0.15 / 0.15 | 1 |
| **the last-sync-exit stamp** | **1.46 / 1.46 / 1.46** | 1 |
| the card gone from the screen | 3.51 / 3.51 / 3.51 | 1 |

Outcomes: completed x1. Payload seeded 616 KiB (RetroArch rewrites the auto-state on exit, so what moves is a little less; the log's rclone line has the bytes).

### Game to game, with the exit sync in flight

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.16 / 0.16 / 0.16 | 1 |
| the relaunch sent | 0.16 / 0.16 / 0.16 | 1 |
| the question answered (STOP IT AND PLAY, D-CLOUD-130) | 1.36 / 1.36 / 1.36 | 1 |
| **the next game's first frame** | **1.01 / 1.01 / 1.01** | 1 |
| the exit sync's stamp | - | 1 |

What the launch did to the sync, from the stamp's token: `?` x1.


renderer: virgl (Mesa Intel(R) Graphics (ARL)). -- the guest's Mesa, from the launch log; display: GL through virgl on /dev/dri/renderD128
