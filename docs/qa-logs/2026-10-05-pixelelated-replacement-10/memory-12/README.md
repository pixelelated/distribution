# Installed emulator and memory qualification

Frozen source d6e8390c93, bundle1c69bcf5. All three original memory phases pass
unchanged strict1024KiB virtual/2048KiB resident growth limits after5warmups:

| Profile | Measured cycles | Virtual growth KiB | Resident growth KiB |
| --- | --- | --- | --- |
| virgl | 10 | 0 | 224 |
| software/Pixman | 10 | -448 | 684 |
| software/Pixman with exit sync | 50 | 0 | 444 |

All55sync stamps, including warmups, are distinct successful completions.
The original CSV tables and stamps are retained; review-results.py independently
recomputes growth and checks the full stamp set. Installed renderer verification
proves virgl retained and software automatically selects Pixman.

Both profiles pass exit-hotkey and time-to-play suites. First-emulator-frame
samples:0.570s virgl,0.636s software; exit-sync1.324s/1.673s; next-game1.012s/
1.011s. These are one-repeat smoke samples, not distributions. Neither fast g2g
sample has a new sync stamp, so neither proves launch during active sync.
Ten actual timing frames were directly inspected; they show emulator startup,
auto-state transitions and returned ES carousel. Early transition captures are
not settled widget-layout proof. GPU viewport533x480 fills640x480panel height
with aspect sidebars as the existing surface check specifies.

The30second example.org sign-in window load passes; peak combined RSS290096KiB
on8GiB. This is a simple public page, not authenticated provider acceptance.

Durable20:40:45/allfour0. Actuald528be cleanup20:41:05 verifies allsix owner/
guest PIDs absent and noQEMU; actual52dd28 at20:41:08 verifies observed backend
3796226 absent. Retained546artifact hashes/163public artifacts, source seals,
completion, backend cleanup and direct-review receipts. Refs #447/#383.
