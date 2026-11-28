# #1477: the end-of-game wait

Packet for [#1477](https://github.com/pixelelated/distribution/issues/1477) (D-CLOUD-198, D-RA-057), 2026-11-28.

## Build 25 (round `75e31d7ee6`, ES `076b52d0c`: the saves wait alone)

- **The 15 s bound worked.**
  - Case A (`time-to-play --only g2g-midsync`, the stall endpoint) relaunched at 0.57 s. The sync was stopped at 16.05 s (stamp `130 cancelled`), and the game's first frame came at 17.5 s, in EN and FR.
  - Case B (the QA WebDAV throttled to 20 KiB/s, a 1 MiB save, the startup sync): the sync was stopped at the bound in EN and FR (`B-en.launch.txt`, `B-fr.launch.txt`: `130 cancelled`).
  - `B-en-after-the-bound.png` shows SYNC SAVES / SKIPPED - YOU STARTED A GAME / THEY GO UP WHEN YOU EXIT THE GAME. The launched file was a placeholder from `seed-device`, not a ROM, so the game quit at once; build 26's case B launches the probe ROM.
- **A defect, fixed in route 16.** `A-en-wait-cut-at-both-edges.png`: the wait's two sentences were drawn on one line and cut at both edges at 640x480. Route 16 puts them on two lines.

## Build 26 (round `6169621a4b`, ES `e67f28e18`: one wait over the end-of-game work)

Its proof is `/workspace/tmp/rocknix-session/p1477-b26.sh`:
- **A:** the midsync cell.
- **B:** a throttled startup sync, with the probe ROM.
- **C:** the achievements' send inside the wait, from one synthetic held award and a loopback stand-in holding the award request 6 s.

It runs in EN and FR, inside `b26-carry.sh`. Its frames are added here once they have been reviewed.

### Build 26 results (all frames reviewed by the OS coordinator)

- **A** (`A-{en,fr}-wait.png`, `A-{en,fr}-game.png`): the two lines fit at 640x480; the stall endpoint's sync was stopped at 15.9 s (`130 cancelled`), and the game's first frame came at 17.5 s.
- **B** (`p1477-bc.sh`, 02:40 UTC; `B-*`): the wait over SYNCING SAVES AT STARTUP / SENDING FILE 1 OF 1. At the bound, SYNC SAVES / SKIPPED - YOU STARTED A GAME, then the game. Stamp `130 cancelled`, RetroArch running afterwards, in EN and FR.
- **C** (`C-*`): the saves sync completed during the wait (`0 completed`), and the page then read OFFLINE ACHIEVEMENTS ARE BEING SENT. / YOUR GAME STARTS WHEN THEY'RE DONE. (FR: LES SUCCÈS HORS LIGNE SONT EN COURS D’ENVOI. / VOTRE JEU DÉMARRE DÈS QU’ILS SONT ENVOYÉS.). The stand-in held the award 12 s, the game started once it had gone, and `raofflineproxy-ctl pending` read 0, in EN and FR.
- **The first B and C run failed its own checks:** case A's `time-to-play` had removed the shared probe ROM path. `b26-guard.sh` held the handheld builds on it (`guard-held.txt`), and `p1477-bc.sh` reran B and C with the ROM put back. The chain that launched the handheld builds, `b26-handhelds.sh`, gated each step on the one before.
