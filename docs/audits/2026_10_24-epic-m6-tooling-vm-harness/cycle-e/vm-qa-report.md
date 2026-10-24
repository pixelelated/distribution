# vm-qa on 069fc27044

started 2026-10-24 22:16 UTC, guest a at :10022, cloud webdav (port 9010, hash=none modtime=no commit=partial bucket=no), image /workspace/artifacts/m6-t1-20261023/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz, display: GL through virgl on /dev/dri/renderD128

BUILD_ID 069fc270442134fe771258418adf4e666e0473fb -- the image names 069fc270442134fe771258418adf4e666e0473fb

ES_SRC /home/max/Development/emulationstation-next.worktrees/qa-integration at 16dbac5211eea7e70db7394372033be2be7df829; the image's build 069fc270442134fe771258418adf4e666e0473fb pins (pin unreadable)

paths: pair /workspace/repos/pixelelated/distribution.worktrees/m6-tooling-vm-harness-659/.qa-scratch/vm-pair; runtime /run/user/1000/pixelelated-vm-1c7e8c12; QA cloud /workspace/repos/pixelelated/distribution.worktrees/m6-tooling-vm-harness-659/.qa-scratch/cloud-qa; scratch /workspace/repos/pixelelated/distribution.worktrees/m6-tooling-vm-harness-659/.qa-scratch/vm-qa-tmp/qa-069fc27044-webdav-a-20261024-221602; key /workspace/repos/pixelelated/distribution.worktrees/m6-tooling-vm-harness-659/.qa-scratch/vm-pair/qa-key -- and this report under the report root /workspace/artifacts/rocknix-images, which stays where the record keeps every run

| suite | result | time | log |
| --- | --- | --- | --- |
| scripts | FAIL (1) | 675s | `scripts.log` |
| lifetime | SKIP (ES_SRC 16dbac5211, image pins unreadable) | 0s | `lifetime.log` |
| wrapper | FAIL (2) | 0s | `wrapper.log` |
| vocabulary | SKIP (ES_SRC 16dbac5211, image pins unreadable) | 0s | `vocabulary.log` |
| french | SKIP (ES_SRC 16dbac5211, image pins unreadable) | 0s | `french.log` |
| quoting | SKIP (ES_SRC 16dbac5211, image pins unreadable) | 0s | `quoting.log` |
| menumap | SKIP (ES_SRC 16dbac5211, image pins unreadable) | 0s | `menumap.log` |
| register | SKIP (ES_SRC 16dbac5211, image pins unreadable) | 0s | `register.log` |
| pair-identity | PASS | 0s | `pair-identity.log` |
| fresh | PASS | 1s | `fresh.log` |
| round-trip | PASS | 85s | `round-trip.log` |
| exit | PASS | 28s | `exit.log` |
| time-to-play | FAIL (1) | 69s | `time-to-play.log` |
| walks | PASS | 1029s | `walks.log` |
| frame-diff | PASS | 12s | `frame-diff.log` |

**FAILED** -- 3 suite(s) failed; see the logs beside this file (exit 1).

finished 2026-10-24 22:47 UTC

bring-up 75s, fixture 6s -- outside the suite rows, so the minutes a reader sums are the run's

tear-down: vm-pair down rc 0

ssh and scp calls cut at the 300 s bound: 0

## time to play -- 069fc27044 on webdav

2026-10-24 22:29 UTC, guest at :10022, cloud `webdav`, payload `full`, 1 repeat(s).

Host state: **vm-qa on serval, guest a**. SSH round trip 5 ms (the launch POST goes over it); one screendump 64 ms, which is the resolution of every frame-derived number below.

Seconds, as median / mean / max.

### UI to game, at rest

| from the press to | median / mean / max | n |
| --- | --- | --- |
| the screen leaving the carousel | 0.10 / 0.10 / 0.10 | 1 |
| the handover (a black screen) | 0.10 / 0.10 / 0.10 | 1 |
| RetroArch existing | 0.55 / 0.55 / 0.55 | 1 |
| **the game's first frame** | **0.69 / 0.69 / 0.69** | 1 |
| RetroArch drawing (200 CPU ticks, or 30 four seconds on) | 4.63 / 4.63 / 4.63 | 1 |

### The exit sync, on its own

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.16 / 0.16 / 0.16 | 1 |
| **the last-sync-exit stamp** | **1.33 / 1.33 / 1.33** | 1 |
| the card gone from the screen | 3.51 / 3.51 / 3.51 | 1 |

Outcomes: completed x1. Payload seeded 612 KiB (RetroArch rewrites the auto-state on exit, so what moves is a little less; the log's rclone line has the bytes).

### Game to game, with the exit sync in flight

| from execute_kill to | median / mean / max | n |
| --- | --- | --- |
| the emulator gone | 0.16 / 0.16 / 0.16 | 1 |
| the relaunch sent | 0.16 / 0.16 / 0.16 | 1 |
| the question answered (STOP IT AND PLAY, D-CLOUD-130) | 1.38 / 1.38 / 1.38 | 1 |
| **the next game's first frame** | **1.01 / 1.01 / 1.01** | 1 |
| the exit sync's stamp | - | 1 |

What the launch did to the sync, from the stamp's token: `?` x1.


**Not a pass:** the kill helper exited 1 in a exit repeat; the kill helper exited 1 in a g2g repeat; a game-to-game row has no exit sync stamp.

renderer: virgl (Mesa Intel(R) Graphics (ARL)). -- the guest's Mesa, from the launch log; display: GL through virgl on /dev/dri/renderD128
