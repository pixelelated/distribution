# T32 (#679): the guest window's plan

**Can this be done on the VM?** Yes, for everything the image draws: the five view styles and the carousel, the cursor and letter logic, the offline scrape's outcome, the IGDB dialog in both locales, the local HTTP API from inside the guest, and the French. Two things are not the guest's:
- **No scraper's success path.** A no-NIC guest reaches no scraper host. ArcadeDB is the one plain-http host, and a stub for it needs a host listener on port 80; this host's `ip_unprivileged_port_start` is 1024, so G-07 is `CANNOT`.
- **No stall or 429.** The https hosts refuse a stub, so G-10 is `CANNOT`; those paths are unit cases (3.13).

Nothing runs on a handheld or against the owner's accounts. No step signs in, so the QA accounts are not needed (D-QA-015, D-QA-016).

- **Image:** the M6 copy `/workspace/artifacts/m6-t2-20261023/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz` (`069fc2704421`). Its `.sha256` holds a bare hash, compared by hand first. It runs on a fresh 16 GB qcow2 of the lane's own under `/workspace/tmp/m6-t32/guest/`, started with `projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm run --headless --daemonize --res 640x480`.
- **Bound:** 35 minutes from START, plus 5 minutes' grace (§ 5 item 2; the steps' bounds sum to 22 minutes without G-07). **What stops it:** at bound plus grace I stop the guest by its pidfile (`tools/vm-stop`, which waits for the exit), whatever step it is in. A step not reached is `CANNOT -- the bound`.
- **Before the guest:** the shared host file read whole at its tail; the census taken; `tools/build-preflight --reclaim-swap` allowed once, before the guest, never beside it.
- **Posts:** `START HH:MM:SS UTC` and `RETURN HH:MM:SS UTC` as the first lines on #679 and in the shared host file, each with the census (`qemu N, compilers N`). The times come from `date -u` in the same command as the post.
- **Every frame is labelled by side.** The image's EmulationStation is M7's composition over the pin. A frame is `pin-binary` evidence only where G-01's digest finds the pin's lines unchanged in the image's binary; otherwise `image`.
- **What the guest changes is the guest's own:** files under `/storage` and `/tmp`, discarded with the disk. The disk is retired after the window, with its path, size and sha recorded (D-INFRA-022).

## The steps, in order

| G | Proof | What is driven | What is read back | Bound (s) |
| --- | --- | --- | --- | ---: |
| G-01 | identity and side | `vm-serial sh 'cat /etc/os-release; fbset'`; the installed ES binary checked for two literals: one the pin carries in the slice (`SAVE STATES (HOLD)`, #210) and one only M7's composition carries | `BUILD_ID`, 640x480; the side every later frame takes | 60 |
| G-02 | the views, L-14, Q5 | `manager.steps`' first two steps (`0-carousel`, `1-list`); GAMELIST VIEW STYLE cycled (`basic`, `detailed`, `video`, `grid`, `gamecarousel`), the hop from USER INTERFACE SETTINGS to THEME CONFIGURATION read on the guest; `shot` per style. **L-14:** 100 screenshots seeded over serial into the SCREENSHOTS system (named for the fixture games), then SCREENSHOTS opened in grid style, timed from the press to the first tiles' frame, against a list of 10; the French frame of `SAVE STATES (HOLD)` | each style's frame; the one list help bar per style; the two timings; the French frame | 240 |
| G-03 | 3.29, the letter jump | on a list with three or more first letters: the next and previous letter keys, `shot` after each | the cursor on the next letter's first game; the wrap from the last letter | 120 |
| G-04 | 3.27, the carousel's fast move | on `0-carousel`, with fewer than ten systems: the fast move backward, `shot`; then forward | a clean wrap, or a wrong system, a blank, or a backtrace in `journalctl -u essway` | 120 |
| G-05 | 3.13, L-05, L-07 | `ip link set eth0 down`; SCRAPER > SCRAPE, ArcadeDB, SCRAPE NOW; `shot` the outcome; the link back | the outcome words (COMPLETED-shaped with nothing scraped is the lead's positive); line 4; `ThreadedScraper::SearchResponse` in the journal; the steps kept under `stage-e/walks/` (Backlog #1190) | 240 |
| G-06 | 3.16's remainder, L-04 | SCRAPER > SCRAPE, IGDB with no client id, SCRAPE NOW, `shot`; B; then `system.language=fr_FR`, ES restarted (back on the last list: one `z`, a frame), the same | `AN ERROR OCCURRED :` and `INVALID CREDENTIALS` in EN and FR; B landing on the only button, framed | 180 |
| G-07 | ArcadeDB against a host stub | -- | `CANNOT`: a listener on host port 80 needs privilege here (`ip_unprivileged_port_start` 1024) | 0 |
| G-08 | the HTTP API (3.21 to 3.26, L-12, L-13, L-19, L-20) | from inside the guest: `wget -qO- http://127.0.0.1:1234/caps`, `/isIdle`; `POST /notify` with a long body; `POST /removegames/<system>` with a path outside the system; one `POST /launch` | `"Version"`; `[ true ]`; the toast's frame against the one-line rule; `204 No game removed`; the launch. The `403` for a non-loopback caller is `CANNOT`: the VM forwards SSH and the profile's services, never 1234 | 120 |
| G-09 | L-08, the stale read | a detailed list over a game with no manual (MANUAL absent); a manual file written over serial and the game's metadata pointed at it with the list open; the list re-entered in the same session; then GAME SETTINGS > UPDATE GAMELISTS, `shot` the carousel and `1-list` | the MANUAL row absent until a launch: L-08's positive, `image` side; the carousel after UPDATE GAMELISTS | 120 |
| G-10 | a stall or 429 inside the scrape | -- | `CANNOT`: the https hosts refuse a stub; 3.13's unit cases | 0 |
| G-11 | close | `tools/vm-stop` on the pidfile; the disk's path, size and sha recorded | `retired.txt`; `qemu 0, compilers 0` | 120 |

Sum of the bounds: 1,320 s (22 minutes), G-07 and G-10 at 0. If the bound comes first, G-09's UPDATE GAMELISTS half, G-04 and G-03 are dropped first; G-01, G-02, G-05, G-06 and G-08 are the ones the leads need most.

**The host proofs, before or beside the window** (stage C, under `stage-c/`, each seen to FAIL against the pin's unfixed extract before it is trusted): the six that FAIL at the pin (3.10, 3.13, 3.16's remainder, 3.27, 3.31, 3.32 at both `atol` sites), then the rest of the 35, built by `tools/t32-build-tests.sh` in T21's and T26's shape.
