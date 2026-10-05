# vm-qa on 69e6039f8f

started 2026-09-29 22:15 UTC, guest a at :10022, cloud webdav (port 9010, hash=none modtime=no commit=partial bucket=no), image /workspace/artifacts/rocknix-images/x64-all-20260929-69e6039f8f/ROCKNIX-GENERIC_X64.x86_64-20260929.img.gz, display: GL through virgl on /dev/dri/renderD128

| suite | result | time | log |
| --- | --- | --- | --- |
| scripts | FAIL (1) | 480s | `scripts.log` |
| lifetime | PASS | 1s | `lifetime.log` |
| wrapper | PASS | 0s | `wrapper.log` |
| vocabulary | PASS | 0s | `vocabulary.log` |
| french | PASS | 0s | `french.log` |
| quoting | PASS | 0s | `quoting.log` |
| menumap | PASS | 0s | `menumap.log` |
| register | PASS | 2s | `register.log` |
| pair-identity | PASS | 1s | `pair-identity.log` |
| fresh | PASS | 0s | `fresh.log` |
| round-trip | PASS | 95s | `round-trip.log` |
| exit | PASS | 29s | `exit.log` |
| time-to-play | PASS | 81s | `time-to-play.log` |
| walks | PASS | 996s | `walks.log` |
| frame-diff | FAIL (1) | 1s | `frame-diff.log` |

**FAILED** -- 2 suite(s) failed; see the logs beside this file.

finished 2026-09-29 22:43 UTC

## time to play -- 69e6039f8f on webdav

2026-09-29 22:26 UTC, guest at :10022, cloud `webdav`, payload `full`, 1 repeat(s).

Host state: **vm-qa on serval, guest a**. SSH round trip 5 ms (the launch POST goes over it); one screendump 62 ms, which is the resolution of every frame-derived number below.

Seconds, as median / mean / max.

### UI to game, at rest

| from the press to | median / mean / max | n |
| --- | --- | --- |
| the screen leaving the carousel | 0.01 / 0.01 / 0.01 | 1 |
| the handover (a black screen) | 0.01 / 0.01 / 0.01 | 1 |
| RetroArch existing | 0.58 / 0.58 / 0.58 | 1 |
| **the game's first frame** | **1.05 / 1.05 / 1.05** | 1 |
| RetroArch drawing (200 CPU ticks, or 30 four seconds on) | 4.58 / 4.58 / 4.58 | 1 |

### The exit sync, on its own

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.22 / 0.22 / 0.22 | 1 |
| **the last-sync-exit stamp** | **2.33 / 2.33 / 2.33** | 1 |
| the card gone from the screen | 4.53 / 4.53 / 4.53 | 1 |

Outcomes: completed x1. Payload seeded 616 KiB (RetroArch rewrites the auto-state on exit, so what moves is a little less; the log's rclone line has the bytes).

### Game to game, with the exit sync in flight

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.21 / 0.21 / 0.21 | 1 |
| the relaunch sent | 0.23 / 0.23 / 0.23 | 1 |
| the question answered (STOP IT AND PLAY, D-CLOUD-130) | 1.41 / 1.41 / 1.41 | 1 |
| **the next game's first frame** | **2.03 / 2.03 / 2.03** | 1 |
| the exit sync's stamp | - | 1 |

What the launch did to the sync, from the stamp's token: `?` x1.


renderer: virgl (Mesa Intel(R) Graphics (ARL)). -- the guest's Mesa, from the launch log; display: GL through virgl on /dev/dri/renderD128
