# vm-qa on 02163b440b

started 2026-10-04 18:20 UTC, guest a at :10022, cloud webdav (port 9010, hash=none modtime=no commit=partial bucket=no), image /workspace/artifacts/pixelelated-candidates/sha256/8e9eb161b8b4ab84b6339ff58d478acf00322f3c8fa70d5c2c4575849c6a149f/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz, display: GL through virgl on /dev/dri/renderD128

| suite | result | time | log |
| --- | --- | --- | --- |
| scripts | PASS | 779s | `scripts.log` |
| lifetime | PASS | 1s | `lifetime.log` |
| wrapper | PASS | 0s | `wrapper.log` |
| vocabulary | PASS | 0s | `vocabulary.log` |
| french | PASS | 0s | `french.log` |
| quoting | PASS | 1s | `quoting.log` |
| menumap | PASS | 0s | `menumap.log` |
| register | PASS | 1s | `register.log` |
| pair-identity | PASS | 1s | `pair-identity.log` |
| fresh | PASS | 1s | `fresh.log` |
| round-trip | PASS | 84s | `round-trip.log` |
| exit | PASS | 28s | `exit.log` |
| time-to-play | PASS | 70s | `time-to-play.log` |
| walks | PASS | 1002s | `walks.log` |
| frame-diff | PASS | 0s | `frame-diff.log` |

**PASSED** -- every suite that ran passed.

finished 2026-10-04 18:53 UTC

## time to play -- 02163b440b on webdav

2026-10-04 18:36 UTC, guest at :10022, cloud `webdav`, payload `full`, 1 repeat(s).

Host state: **vm-qa on serval, guest a**. SSH round trip 6 ms (the launch POST goes over it); one screendump 62 ms, which is the resolution of every frame-derived number below.

Seconds, as median / mean / max.

### UI to game, at rest

| from the press to | median / mean / max | n |
| --- | --- | --- |
| the screen leaving the carousel | 0.09 / 0.09 / 0.09 | 1 |
| the handover (a black screen) | 0.09 / 0.09 / 0.09 | 1 |
| RetroArch existing | 0.48 / 0.48 / 0.48 | 1 |
| **the game's first frame** | **0.68 / 0.68 / 0.68** | 1 |
| RetroArch drawing (200 CPU ticks, or 30 four seconds on) | 4.56 / 4.56 / 4.56 | 1 |

### The exit sync, on its own

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.16 / 0.16 / 0.16 | 1 |
| **the last-sync-exit stamp** | **1.47 / 1.47 / 1.47** | 1 |
| the card gone from the screen | 3.52 / 3.52 / 3.52 | 1 |

Outcomes: completed x1. Payload seeded 616 KiB (RetroArch rewrites the auto-state on exit, so what moves is a little less; the log's rclone line has the bytes).

### Game to game, with the exit sync in flight

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.16 / 0.16 / 0.16 | 1 |
| the relaunch sent | 0.17 / 0.17 / 0.17 | 1 |
| the question answered (STOP IT AND PLAY, D-CLOUD-130) | 1.36 / 1.36 / 1.36 | 1 |
| **the next game's first frame** | **1.02 / 1.02 / 1.02** | 1 |
| the exit sync's stamp | - | 1 |

What the launch did to the sync, from the stamp's token: `?` x1.


renderer: virgl (Mesa Intel(R) Graphics (ARL)). -- the guest's Mesa, from the launch log; display: GL through virgl on /dev/dri/renderD128
