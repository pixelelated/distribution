# vm-qa on 1e6a156b54

started 2026-10-04 19:55 UTC, guest a at :10022, cloud webdav (port 9010, hash=none modtime=no commit=partial bucket=no), image /workspace/artifacts/pixelelated-candidates/sha256/a179bd73a732f49c4219177c89a860d561dad4d16a3467aae2cbafc15152b3ea/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz, display: GL through virgl on /dev/dri/renderD128

| suite | result | time | log |
| --- | --- | --- | --- |
| scripts | PASS | 777s | `scripts.log` |
| lifetime | PASS | 1s | `lifetime.log` |
| wrapper | PASS | 0s | `wrapper.log` |
| vocabulary | PASS | 0s | `vocabulary.log` |
| french | PASS | 1s | `french.log` |
| quoting | PASS | 0s | `quoting.log` |
| menumap | PASS | 0s | `menumap.log` |
| register | PASS | 2s | `register.log` |
| pair-identity | PASS | 0s | `pair-identity.log` |
| fresh | PASS | 1s | `fresh.log` |
| round-trip | PASS | 84s | `round-trip.log` |
| exit | PASS | 28s | `exit.log` |
| time-to-play | PASS | 70s | `time-to-play.log` |
| walks | PASS | 1008s | `walks.log` |
| frame-diff | PASS | 0s | `frame-diff.log` |

**PASSED** -- every suite that ran passed.

finished 2026-10-04 20:28 UTC

## time to play -- 1e6a156b54 on webdav

2026-10-04 20:11 UTC, guest at :10022, cloud `webdav`, payload `full`, 1 repeat(s).

Host state: **vm-qa on serval, guest a**. SSH round trip 5 ms (the launch POST goes over it); one screendump 61 ms, which is the resolution of every frame-derived number below.

Seconds, as median / mean / max.

### UI to game, at rest

| from the press to | median / mean / max | n |
| --- | --- | --- |
| the screen leaving the carousel | 0.01 / 0.01 / 0.01 | 1 |
| the handover (a black screen) | 0.01 / 0.01 / 0.01 | 1 |
| RetroArch existing | 0.50 / 0.50 / 0.50 | 1 |
| **the game's first frame** | **0.66 / 0.66 / 0.66** | 1 |
| RetroArch drawing (200 CPU ticks, or 30 four seconds on) | 4.53 / 4.53 / 4.53 | 1 |

### The exit sync, on its own

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.16 / 0.16 / 0.16 | 1 |
| **the last-sync-exit stamp** | **1.46 / 1.46 / 1.46** | 1 |
| the card gone from the screen | 3.51 / 3.51 / 3.51 | 1 |

Outcomes: completed x1. Payload seeded 616 KiB (RetroArch rewrites the auto-state on exit, so what moves is a little less; the log's rclone line has the bytes).

### Game to game, with the exit sync in flight

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.16 / 0.16 / 0.16 | 1 |
| the relaunch sent | 0.17 / 0.17 / 0.17 | 1 |
| the question answered (STOP IT AND PLAY, D-CLOUD-130) | 1.38 / 1.38 / 1.38 | 1 |
| **the next game's first frame** | **1.02 / 1.02 / 1.02** | 1 |
| the exit sync's stamp | - | 1 |

What the launch did to the sync, from the stamp's token: `?` x1.


renderer: virgl (Mesa Intel(R) Graphics (ARL)). -- the guest's Mesa, from the launch log; display: GL through virgl on /dev/dri/renderD128
