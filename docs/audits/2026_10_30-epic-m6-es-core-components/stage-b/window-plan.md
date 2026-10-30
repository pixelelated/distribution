# T34 (#681) guest window plan

Asked for on #681 at stage B's end and as a line in `/workspace/tmp/m7-m6-host-coordination.txt`. It runs only on the coordinator's grant there and in that file's queue, after every M7 window (the host file's 14:21 entry).

- **Bound:** 30 minutes, plus 5 of grace, for a plan of **1410 s** (the brief's § 5 item 2: `printf '%s\n' 60 240 120 120 180 120 0 180 90 0 180 120 | awk '{s+=$1} END {print s}'`, re-run here). Two boots of one disk: 640x480 first, then 1280x800 for G-11.
- **The image:** `/workspace/artifacts/m6-t2-20261023/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz` (2,122,289,964 bytes; M6's copy of `069fc2704421`). It is identified first by two literals, `BUILD_ID` from the guest's `/etc/os-release` and the file name.
- **The disk:** made from the image under `/workspace/tmp/m6-t34/guest/` before START, enlarged to 16 GiB (a smaller disk breaks the first boot, `generic-x64-vm-testing.md`), with its path, size and sha256 recorded. It is retired after G-12, with path, size and sha in `00` (D-INFRA-022).
- **The runs:** `projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm run --headless --daemonize --res 640x480 <disk>` (#1141: `vm-pair` has no size option), then `tools/vm-serial` for the shell and `tools/vm-visual-qa` for frames. The walks' steps go under `stage-e/walks/`, never `tools/`.
- **The stop:** `tools/vm-stop` on the guest's pidfile, never a pattern. At START a detached timer is armed to run that same stop at the bound plus grace (35 minutes after START), and the START post names it with its PID. A RETURN post ends the window, with the census.
- **The post contract:** `START HH:MM:SS UTC` and `RETURN HH:MM:SS UTC` as each post's first line, each with the census (`qemu N, compilers N`), and a line in the host file beside each.
- **Every frame** is labelled `image` (the guest's EmulationStation is M7's composition) or `pin-binary` (only where G-01's digest finds the pin's lines unchanged in the image's binary). A fix's frame is `fix-walk-pending-image`. Pixels are measured by a reader (a stdlib `zlib` PNG reader), never by eye.
- **No accounts:** no row needs the QA accounts, and the owner's are never used.

| G | What only the running image shows | Bound (s) |
| --- | --- | ---: |
| G-01 | identity and side: `BUILD_ID`, `fbset` (640x480), the theme, whether a theme draws a grid, the face path for `tools/font-stems`; the ES binary's digest against the pin's lines | 60 |
| G-02 | the card at 0.9 of the width, centred, opaque over box art: edges at x 32 and x 608, a panel-colour pixel over the art (the startup sync card after `default-pre` with the WebDAV stanza) | 240 |
| G-03 | the button bar's gap at 640 (14 px, `0.022 x 640`) and a YES/NO box's one CHOOSE (MAIN MENU > QUIT > RESTART EMULATIONSTATION, declined with B) | 120 |
| G-04 | a dimmed row at alpha 0x50 (the CLOUD page, unseeded), then the same page under French with the `Unknown help icon` log count (L-01's positive) | 120 |
| G-05 | the tab strip as a focus stop (MAIN MENU > SCRAPER): four frames and the wrap; the page reopened once for L-02's pair | 180 |
| G-06 | `canMoveCursor` on a one-button dialog: `OK` and no `CHOOSE` (the dialog named in the START post) | 120 |
| G-07 | a `MultiLineMenuEntry` refreshed hundreds of times: `CANNOT` in one window; the proof is 3.4 | 0 |
| G-08 | the grid view at 640x480 if G-01 finds a grid theme, else `CANNOT` with G-01's grep line | 180 |
| G-09 | a slider's glued suffix and `Auto` if an auto slider is reachable | 90 |
| G-10 | a video component's lifetime: `CANNOT` (no media); the detached thread is § The lifetimes' read | 0 |
| G-11 | the second size, 1280x800, on the same disk: the bar's gap (28 px), the help bar, G-05's strip | 180 |
| G-12 | close: `tools/vm-stop` on the pidfile; the disk's size and sha; `qemu 0, compilers 0` | 120 |
