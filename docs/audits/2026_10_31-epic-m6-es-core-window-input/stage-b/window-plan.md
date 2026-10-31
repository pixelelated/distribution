# T35's guest window: the plan and its bound (#682, brief § 5 item 2)

**Can this be done on the VM?** Yes: every row below runs on one GENERIC_X64 guest. The three rows the guest cannot run say why: G-03 (no two-toast source inside one card), G-10 (no gamepad device), and G-08's hold if the monitor cannot hold a key.

- **The bound: 30 minutes, plus 5 of grace** (35 minutes, 2,100 s, from START to RETURN). The plan sums to **1,560 s**, by the brief's own command re-run at stage B: `printf '%s\n' 60 240 0 120 120 180 120 180 240 0 180 120 | awk '{s+=$1} END {print s}'` printed `1560`.
- **The image:** `/workspace/artifacts/m6-t2-20261023/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`, 2,122,289,964 bytes (`ls -l`, 06:30 UTC). It is checked against its `.sha256` before the first boot. One working disk is made from it under the scratch directory, and nothing beside it in that folder is touched (`t2.qcow2` is T2's).
- **Two boots of the one disk:** first at 640x480 (`generic-x64-vm run --headless --daemonize --res 640x480`, #1141), then at 1280x800 for G-11. Each verdict is labelled by side: `image`, or `pin-binary` only where the digest finds the pin's lines unchanged.
- **The timer:** at START a detached `setsid` process sleeps 2,100 s, then runs `tools/vm-stop` on the guest's pidfile. The START post names its PID (`engineering-practices.md` § A granted guest window names what stops the guest, #1135). At RETURN it is stopped by that PID.
- **Before the guest:** the host file is read in the minute before START, with the census (`qemu N, compilers N`). `tools/build-preflight --reclaim-swap` is allowed once, before the guest and never beside it.
- **The posts:** `START HH:MM:SS UTC` and `RETURN HH:MM:SS UTC` each open a post on #682 and add a line to `/workspace/tmp/m7-m6-host-coordination.txt`, each with the census. RETURN lands inside the bound plus grace.
- **The stop:** `tools/vm-stop` by the pidfile, never a pattern. The disk is retired with its path, size and sha (D-INFRA-022). The leftover check reads `qemu 0, compilers 0`.
- **No account:** the QA accounts are needed by no row. The WebDAV stanza G-02 and G-09 seed is the host's own `tools/cloud-test-backend`. No owner account, device, M7 root, worktree or prep directory is touched.

| G | What only the running image shows | How | Bound (s) |
| --- | --- | --- | ---: |
| G-01 | identity and side; the theme and the face; whether the user `es_input.cfg` exists before configuration (L-07); the shipped `inputAction` count (L-08); `ldd ... \| grep -c udev` (the `UDEV_FOUND` answer) | `vm-serial sh` with the brief's line; the ES binary's digest against the pin's lines | 60 |
| G-02 | a toast held under the startup sync card, then drawn whole; the card's edges at x 32 and x 608 (a stdlib PNG reader) | `default-pre` with the WebDAV stanza; reboot; **UPDATE GAMELISTS** pressed while the card is up (the games-list toast, `Window.cpp:1505`), or a REBOOT REQUIRED toggle if the press cannot land inside the card (the choice named in START); `shot` every 0.4 s for 6 s | 240 |
| G-03 | two toasts under a card, newest first (L-01) | `CANNOT`: no two-toast source the keyboard can fire inside one card; the proof is 3.14 | 0 |
| G-04 | YES/NO: back lands on NO; the help bar under a second page | MAIN MENU > QUIT > RESTART EMULATIONSTATION; `shot`; `z`; `shot`; `pgrep -c emulationstation` before and after | 120 |
| G-05 | a two-button dialog with neither OK nor NO: back takes the last button | the candidate read from the map before START, named there; else `CANNOT` with the candidates listed | 120 |
| G-06 | the keyboard at 640: key gap, START, ESC, `x` clears and commits (L-14) | `to-change-cloud-folder`, `confirm-cloud-folder`; reopen; `key esc`; `shot`; reopen; `key s`; `shot`; `default-pre` reseeds the folder after | 180 |
| G-07 | the dialogs and the keyboard in French | `systemctl stop essway`; `system.language=fr_FR` over serial; ES started; G-04's box, G-06's keyboard, G-08's detect page | 120 |
| G-08 | the detect sentence, the hold, the 14 prompts and `GAMEPAD %i` (L-17) | CONTROLLER & BLUETOOTH SETTINGS' configure row (named in START); `sendkey x 1000` once over the monitor socket; `shot`; else `CANNOT` with the harness gap named | 180 |
| G-09 | the screensaver's timer and the eaten wake press; the screensaver over the transfer page (#1305's window half) | SCREENSAVER AFTER at its minimum; wait; `shot`; `key shift`; `shot`; `key down`; `shot`; BACK UP SAVES TO THE CLOUD left on its outcome; wait; `shot` | 240 |
| G-10 | a pad's hot-plug toasts and rebuild | `CANNOT`: no gamepad device on the guest; an open item to test, the harness gap named | 0 |
| G-11 | the second size: the keyboard, the wide box, the card; T34 PL-05's tabbed page at 1280x800 (L-28) | `tools/vm-stop`; the same disk at `--res 1280x800`; G-06's keyboard, G-04's box, SCRAPER's tabs; `shot` each | 180 |
| G-12 | close | `tools/vm-stop` on the pidfile; the disk's size and sha; `qemu 0, compilers 0`; `retired.txt` | 120 |
