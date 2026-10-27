# T31 (#678): the guest window's plan

**Can this be done on the VM?** Yes: each step below is a GENERIC_X64 fact, with the same EmulationStation binary, the same scripts and a 640x480 panel. Two leads are not the guest's:
- L-02's row appears only with `DEVICE_ANALOG_STICKS_LED_CONTROL=true` (`GuiMenu.cpp:2197`);
- L-10's axis cannot be sent through the guest's QMP keys.

Both are proved on the host. Nothing runs on a handheld or against the owner's accounts. No hosted account is used: no step signs in, so the QA accounts are not needed.

- **Image:** the M6 copy `/workspace/artifacts/m6-t2-20261023/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`, its `.sha256` checked first. It runs on a fresh 16 GB qcow2 of the lane's own under `/workspace/tmp/m6-t31/guest/`, started at 640x480 (`generic-x64-vm run --headless --daemonize --res 640x480`, #1141). One boot.
- **Bound:** 45 minutes from START, plus 5 minutes' grace. **What stops it:** at bound plus grace I stop the guest by its pidfile (`tools/vm-stop`, which waits for the exit), whatever step it is in. A step not reached is `CANNOT -- the bound`. The watch is active supervision: I read the guest's pidfile and the clock at most 60 s apart for the whole window. Nothing alerts if the session disconnects.
- **Posts:** `START HH:MM:SS UTC` and `RETURN HH:MM:SS UTC` as the first lines on #678 and in the shared host log, each with the census (qemu live, compilers). The times come from `date -u` in the same command as the post.
- **Every frame is labelled by side.** The image's EmulationStation is M7's composition over the pin, so a frame is `image` evidence unless G01's literal check finds the pin's lines unchanged there (`pin-binary`).
- **What the guest changes is the guest's own:** files under `/storage` and `/tmp`, bind mounts that the reboot-free stop discards with the disk. The disk is retired after the window, with its path, size and sha recorded (D-INFRA-022).

## The steps, in order

| Step | Proof | Image versus tree, first | What is read back |
| --- | --- | --- | --- |
| G01 | identity | -- | `BUILD_ID`, `BUILD_BRANCH`; `fbset` 640x480. The installed ES by two literals (`generic-x64-vm-testing.md`): M7's composition's `Pending achievements stay` and the pin's `SKIPPED - YOU CANCELLED IT`. Then the leads' own literals (`strings \| grep -c`): `THE BIOS CHECK RETURNED NOTHING`, `MOONLIGHT GAME STREAMING`, `Unpaired and settings cleared`. Whether `/usr/bin/moonlight`, `/usr/bin/rocknix-systems` and `/usr/bin/analog_sticks_ledcontrol` exist |
| G02 | L-01 (START drops the page) | -- | SCRAPER > OPTIONS: toggle OVERWRITE NAMES, press START (CLOSE). Then `ScrapeNames` in `es_settings.cfg` (with its mtime) before and after: unchanged is the lead. Control: the same toggle, then BACK; the key moves |
| G03 | L-16 (tab-switch writes) | -- | SCRAPER opened from the main menu: SCRAPE → OPTIONS → ACCOUNTS → BACK with no change, `es_settings.cfg`'s mtime before and after each move. Then once with GAMES TO SCRAPE FOR changed. On a first visit, the `ScraperSystems` line (L-15's second half) |
| G04 | L-09, the scrape page | the literals (G01) | network down for the guest's ES (`ip link set dev eth0 down`, restored after). SCRAPE NOW over one system with games: SCRAPING GAMES runs, then its finished frame. The words on lines 1, 4 and 5. Then B: the outcome dismissed; the frame after |
| G05 | L-12 (the BIOS check) | -- | BIOS CHECK's list frame and one system's DETAILS (EN). Then `/usr/bin/rocknix-systems` shadowed by a bind-mounted script that exits 1, REFRESH: the frame (THE BIOS CHECK RETURNED NOTHING?). Then unmounted |
| G06 | L-13 (COPY TO FREE SLOT) | -- | the walk `manager.steps` to the manager over a game with one state seeded (`TTProbe.gb`, the artifact folder's). Then W-5's shape: the save-state directory bind-mounted read-only, X (COPY TO FREE SLOT), the frame after, the directory listed. Unmounted. Then a large state (64 MB, `dd`), X timed from the press to the next frame. The help bar and the last tile at 640x480 |
| G07 | back landings (Q1) | -- | the frame after B on each of: the manager's DELETE (YES/NO), GAME OPTIONS' DELETE GAME (YES/NO), CONTROLLER MAPPING's OK/CANCEL (L-19: what B starts), SCRAPER's WARNING if reachable |
| G08 | L-03 (relay change) | -- | NETPLAY SETTINGS: ENABLE NETPLAY toggled, then USE RELAY SERVER moved one step (the page reopens), then BACK. `global.netplay` and `global.netplay.relay` in `system.cfg` through the filter (`grep -v -i -E 'key\|pass\|token\|user\|psk'`, the two keys only) |
| G09 | L-05 and L-06 (Moonlight) | the literals (G01) | MOONLIGHT GAME STREAMING's frame. **L-06:** `~/.config/Moonlight Game Streaming Project/Moonlight.conf` and `~/.cache/Moonlight Game Streaming Project/` seeded (empty files of the guest's own), UNPAIR: the box's frame, and both directories listed after. **L-05:** SERVER IP set to `127.0.0.1;touch /tmp/t31-canary` on the guest's own `system.cfg`, PAIR WITH SERVER: `ls -l /tmp/t31-canary`, then the key reset. `moonlight` pairs with nothing (no server answers on the guest) |
| G10 | L-18 (the viewer's first open) | -- | the screenshot viewer opened over the seeded library: the time from the press to the first tiles' frame, the first open and a second |
| G11 | the stale read (Q4) | -- | GAME OPTIONS over a game with no manual (the MANUAL row absent). With ES running, the game's `manual` metadata pointed at a file created then; GAME OPTIONS again in the same session: does the row appear? (the remembered miss) |
| G12 | French | -- | `system.language=fr`, ES restarted: BIOS CHECK (L-11's `SUR ... MANQUANT`), the scrape page's finished frame if G04 is repeatable within the bound, MOONLIGHT's page (L-07), the manager. Strings read back from the frames |
| G13 | cleanup | -- | the guest stopped by its pidfile; the qcow2 removed with its path, size and sha recorded; `pgrep -x qemu-system-x86` reads 0 for the lane; the leftover check |

If the bound comes first, G10 to G12 are dropped first. G01 to G06 are the ones the leads need most.

**The host proofs, run before or beside the window** (stage C, under the audit folder's `stage-c/`, each seen to FAIL against the pin's extract before a constructed negative is trusted):
- L-01: `GuiSettings::input`/`close`/`save` extracted, over doubled stores and a doubled window.
- L-02: the LED page's lambda and `GuiSettings::save`'s early return.
- L-03: the relay callback and `close()`.
- L-05: the Moonlight command built as written and run through `/bin/sh -c` in bubblewrap (`--clearenv`) with a recording stub and a canary.
- L-06: the two `rm` commands over a fake HOME in bubblewrap.
- L-09: `outcomeWord` and the finished rows over a `progress()` double.
- L-10: `input` over an axis event.
- L-12: `loadList` over an empty vector from a doubled `getBiosInformations`.
- L-14: `savesTreeBusy` over a lock it cannot open.
- L-22: `GuiLoading.h` under `-fsanitize=thread` with doubles.
