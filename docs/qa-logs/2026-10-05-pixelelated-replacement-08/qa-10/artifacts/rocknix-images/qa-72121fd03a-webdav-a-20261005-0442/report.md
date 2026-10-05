# vm-qa on 72121fd03a

started 2026-10-05 04:42 UTC, guest a at :10022, cloud webdav (port 9010, hash=none modtime=no commit=partial bucket=no), image /workspace/artifacts/pixelelated-candidates/sha256/84a794165a6e421cd1aa1dd6d37b97b257c700738c0a53edd282475ecd4780e9/pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz, display: GL through virgl on /dev/dri/renderD128

| suite | result | time | log |
| --- | --- | --- | --- |
| scripts | PASS | 779s | `scripts.log` |
| lifetime | PASS | 0s | `lifetime.log` |
| wrapper | PASS | 1s | `wrapper.log` |
| vocabulary | PASS | 0s | `vocabulary.log` |
| french | PASS | 0s | `french.log` |
| quoting | PASS | 0s | `quoting.log` |
| menumap | PASS | 0s | `menumap.log` |
| register | PASS | 2s | `register.log` |
| pair-identity | PASS | 1s | `pair-identity.log` |
| fresh | PASS | 0s | `fresh.log` |
| round-trip | PASS | 85s | `round-trip.log` |
| exit | PASS | 28s | `exit.log` |
| time-to-play | PASS | 69s | `time-to-play.log` |
| walks | PASS | 1008s | `walks.log` |
| frame-diff | PASS | 1s | `frame-diff.log` |

**PASSED** -- every suite that ran passed.

finished 2026-10-05 05:15 UTC

## time to play -- 72121fd03a on webdav

2026-10-05 04:57 UTC, guest at :10022, cloud `webdav`, payload `full`, 1 repeat(s).

Host state: **vm-qa on serval, guest a**. SSH round trip 5 ms (the launch POST goes over it); one screendump 60 ms, which is the resolution of every frame-derived number below.

Seconds, as median / mean / max.

### UI to game, at rest

| from the press to | median / mean / max | n |
| --- | --- | --- |
| the screen leaving the carousel | 0.10 / 0.10 / 0.10 | 1 |
| the handover (a black screen) | 0.10 / 0.10 / 0.10 | 1 |
| RetroArch existing | 0.58 / 0.58 / 0.58 | 1 |
| **the game's first frame** | **0.80 / 0.80 / 0.80** | 1 |
| RetroArch drawing (200 CPU ticks, or 30 four seconds on) | 4.63 / 4.63 / 4.63 | 1 |

### The exit sync, on its own

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.17 / 0.17 / 0.17 | 1 |
| **the last-sync-exit stamp** | **1.35 / 1.35 / 1.35** | 1 |
| the card gone from the screen | 3.51 / 3.51 / 3.51 | 1 |

Outcomes: completed x1. Payload seeded 616 KiB (RetroArch rewrites the auto-state on exit, so what moves is a little less; the log's rclone line has the bytes).

### Game to game, with the exit sync in flight

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.17 / 0.17 / 0.17 | 1 |
| the relaunch sent | 0.17 / 0.17 / 0.17 | 1 |
| the question answered (STOP IT AND PLAY, D-CLOUD-130) | 1.36 / 1.36 / 1.36 | 1 |
| **the next game's first frame** | **1.01 / 1.01 / 1.01** | 1 |
| the exit sync's stamp | - | 1 |

What the launch did to the sync, from the stamp's token: `?` x1.


renderer: virgl (Mesa Intel(R) Graphics (ARL)). -- the guest's Mesa, from the launch log; display: GL through virgl on /dev/dri/renderD128
