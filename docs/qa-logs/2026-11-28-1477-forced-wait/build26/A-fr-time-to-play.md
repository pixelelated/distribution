# time to play -- 6169621a4b on webdav

2026-11-28 01:57 UTC, guest at :10022, cloud `webdav`, payload `full`, 1 repeat(s).

Host state: **#1477 case A fr, build 26**. SSH round trip 5 ms (the launch POST goes over it); one screendump 60 ms, which is the resolution of every frame-derived number below.

Seconds, as median / mean / max.

## Game to game over a running exit sync (#1012)

| row | the relaunch landed over | relaunch sent (s) | answer sent (s) | question frame | stamp token | cancellation lines |
| --- | --- | --- | --- | --- | --- | --- |
| m1-exit | sync-running | 0.70 | - | m1-exit-wait.png | cancelled | [2026-11-27 20:58:30] [INFO] [cloud_backup] Script completed in 16 seconds with exit code 130 |

The answer is pressed blind, half a second after the relaunch: a row shows the question only through its question frame, which is read, and the sync's cancellation only through its own log lines.


**Not an exclusive benchmark:** no inherited host reservation (RASTERATOPS_BUILD_RUN=unset); host load at start 0.98 5.76 5.63 1/2430 3439456. A cell within its budget stands; one over it is re-run before it is believed.
