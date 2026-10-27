# T33 (#680): the guest window's plan

**Can this be done on the VM?** Yes, for everything the image draws or writes:
- a custom collection made, shown and toggled;
- UPDATE GAMELISTS over a seeded library;
- a `gamelist.xml` written, and a second one written under it while ES runs;
- the screensaver starting and stopping;
- the key-to-pad editor and its file.

The host carries every read, table and unit case (`02`). Four things a no-NIC guest cannot show. Each is a unit lead or a named harness gap, not a device task (`bugs-are-agent-first.md` rule 3):
- **The content installer's download** (G-07 `CANNOT`). Every branch is `ApiSystem::installBatocera*` over the network.
- **NetworkThread's three checks** (G-09 `CANNOT`). UPDATE AVAILABLE needs the network, the token check an account (D-QA-016; no row grows one), and the pads battery a pad.
- **The screensaver's video and slideshow modes.** The fixture has no media.
- **The atomicity of the gamelist write** (G-05 `CANNOT`). There is no fault seam; 3.13 is its unit case.

Nothing runs on a handheld or against the owner's accounts. No step signs in, so the QA accounts are not needed (D-QA-015).

## Bound and conditions

These follow brief § 5 item 2, which keeps T13's shape:
- **Image:** the M6 copy `/workspace/artifacts/m6-t2-20261023/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`. Its identity sidecar is beside it. It runs on a fresh disk, one boot, started at 640x480 (`generic-x64-vm run --headless --daemonize --res 640x480`, #1141).
- **The image is identified first:** `BUILD_ID` from `/etc/os-release` and the file name, before any other step.
- **Bound:** 25 minutes from START, plus 5 minutes' grace. The steps' bounds sum to 1,260 s by the awk line at the end.
- **What stops it:** at bound plus grace I stop the guest by its pidfile (`tools/vm-stop`, which waits for the exit), whatever step is running. A kill by pattern is never used.
- **Before the guest:**
  - the shared host file is read at its tail, with the time of the read;
  - the census is taken;
  - `tools/build-preflight --reclaim-swap` is allowed once, before the guest, never beside it.
- **Posts:** `START HH:MM:SS UTC` and `RETURN HH:MM:SS UTC` as the first line of each post on #680 and as a line in the shared host file, each with the census (`qemu N, compilers N`). The times come from `date -u` in the same command as the post.
- **Every frame is labelled by side.** The image's EmulationStation is M7's composition over the pin. A frame is `pin-binary` evidence only where G-01's digest finds the pin's lines unchanged in the image's binary; otherwise it is `image`. A fix's frame is `fix-walk-pending-image`.
- **What the guest changes is the guest's own:** files under `/storage` and `/tmp`, discarded with the disk. The disk is retired after the window, with its path, size and sha recorded (D-INFRA-022).

## The steps, in order (brief § 5 item 2, word for word)

| G | Behaviour only the running image shows | Walk or serial command | Expected frame or line | Bound (s) |
| --- | --- | --- | --- | ---: |
| G-01 | identity and side | `vm-serial sh 'cat /etc/os-release; fbset'`; the ES binary's digest against the pin's lines (T26's `g01-identity.txt` shape) | `BUILD_ID=...`, `640x480`; every frame labelled `image` or `pin-binary` | 60 |
| G-02 | a custom collection created, enabled, shown and toggled (L-06, L-15) | the on-screen keyboard has no walk (T32 § 5.1), so seed it: `vm-serial sh 'printf "%s\n" /storage/roms/<sys>/<rom> > <collections folder>/custom-t33.cfg'` (the folder from `getCollectionsFolder` `:1518` read on the guest; the file shape from `saveCustomCollection` `:333-357` read first), ES restarted (`generic-x64-vm-testing.md:382`: back on the last list -- one `z`, a frame, then drive), MAIN MENU > GAME COLLECTION SETTINGS > COLLECTIONS TO DISPLAY, tick `t33`, back; `shot` the carousel and the list; then SELECT on the game inside the collection > ADD TO CUSTOM COLLECTION (menu map `:704`) to remove it, `shot`, and `journalctl -u essway` read for `start_es.sh`'s backtrace (the bundle view is assumed to be what the collection opens in at the image's settings; the lane reads `reloadCollection`'s callers on the image's binary, G-01's digest, and labels the frame `image`) | the collection in `SystemView` and its one game in the list (`populateCustomCollection` `:1103`); the file read back over serial lacking the path after the toggle (`toggleGameInCollection` `:671`); a clean list after the removal, or the backtrace (L-06's positive) -- `image` side | 240 |
| G-03 | UPDATE GAMELISTS over a seeded library, the index card, and the stem walk (L-04, L-02) | three zero-byte ROM stubs with valid extensions seeded under `/storage/roms/<sys>/` over serial (`loadGamelistFile` `+79-83` refuses a path that does not exist); N capture stubs under the SCREENSHOTS source (N the lane's, inside the bound); GAME SETTINGS > UPDATE GAMELISTS (`guis/GuiCollectionSystemsOptions.cpp:368`); `/isIdle` waited for (D-QA-057: the installer, the hasher); `shot` the carousel and `1-list`; then a press on SCREENSHOTS timed to its first frame (`tools/time-to-play`'s shape); `stat` of `/var/log/exec.log` | the three stubs in the list; with INDEX NEW GAMES on (menu map `:625`) the `INDEXING COMPLETED. UPDATE ...` toast (`ThreadedHasher.cpp:146`) against the one-line rule; the SCREENSHOTS press-to-frame number for the retro -- `image` side | 180 |
| G-04 | a `gamelist.xml` written and its shape; the stale read (L-05) | one stub marked FAVORITE through SELECT; a `gamelist.xml` for a second system written over serial while ES runs (the restore's shape without the cloud); QUIT > RESTART EMULATIONSTATION (the clean exit writes dirty files, `updateGamelist` `:374`); `vm-serial sh 'cat /storage/roms/<sys>/gamelist.xml; ls <recovery>/<sys>'` (`getGamelistRecoveryPath` `:22`); the second system's file diffed against the written bytes | `<gameList><game><path>./<stub></path>...<favorite>true</favorite>` -- relative path (`+283`), only non-default fields (`ignoreDefaults` true at `:261`), the recovery directory empty after the clean exit (menu map `:626`); the second file unchanged or overwritten (L-05's positive, read both ways) -- `image` side | 180 |
| G-05 | the in-place write's window (`doc.save_file` `:474`) | -- | `CANNOT` on the guest without a fault seam; the lead stays a unit case for the shape (3.13) and a review note for the atomicity | 0 |
| G-06 | the screensaver starting and stopping | with ES stopped (`generic-x64-vm-testing.md:1145`, `:1155`): `ScreenSaverTime` one minute and `ScreenSaverBehavior` `dim` in `es_settings.cfg` over serial, ES started, 70 s waited, `shot`; `wake` (the `wake` step, for which the harness sends `shift`), `shot`; once more with `black` | a dimmed frame then the same screen awake; a black frame; `journalctl -u essway` quiet (`Scripting::fireEvent("screensaver-start")` runs nothing unless a script exists); `random video` and `slideshow` not in this window -- `image` side | 300 |
| G-07 | the content installer's card | -- | `CANNOT` on a no-NIC guest; the card's title `DOWNLOADING <n>` (`:78`) and the toasts (`:140`, `:159`, `:178`, `:214`, `:232`) read as strings | 0 |
| G-08 | the key-to-pad editor and its file (L-28) | on a stub game, SELECT > KEYBOARDTOPADS (menu map `:707`, upstream, tab strip under #63); one mapping set, saved; `shot` the editor; `vm-serial sh 'cat <the .keys file>'` (its path from `save` `:328` read first); then one unknown trigger name written into the file over serial, ES restarted, the editor reopened | the editor frame at 640x480; a JSON with one player array holding `type`, `trigger`, `target` (`:250-288`); the unknown trigger absent from the reopened editor with no word said (L-28's positive) -- `image` side | 180 |
| G-09 | NetworkThread's checks | -- | `CANNOT` on this guest (above); the retry schedule is `CheevosRetry`'s 7 cases | 0 |
| G-10 | close | `tools/vm-stop` on the pidfile; the disk's size and sha; `qemu 0, compilers 0` | `retired.txt`; the leftover check | 120 |

The sum, by `awk -F'|' '/^\| G-/ {s+=$(NF-1)} END {print s}' stage-b/window-plan.md`: 1260 (s), 21 minutes, the brief's figure.
