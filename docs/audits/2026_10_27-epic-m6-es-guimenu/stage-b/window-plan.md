# T26 (#673): the guest window's plan

**Can this be done on the VM? Yes.** Every step below is a GENERIC_X64 fact: the
same EmulationStation binary, the same scripts, a 640x480 panel. Nothing runs
on a handheld or against the owner's accounts; no hosted account is used (the
QA accounts are not needed for any step here).

- **Image:** the M6 copy `/workspace/artifacts/m6-t2-20261023/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`, its `.sha256` checked first, on a fresh 16 GB qcow2 of the lane's own under `/workspace/tmp/m6-t26/guest/`, started at 640x480 (`generic-x64-vm run --headless --daemonize --res 640x480`, #1141). One boot.
- **Bound:** 45 minutes from START, plus 5 minutes' grace. **What stops it:** at bound plus grace I stop the guest by its pidfile (`tools/vm-stop`, which waits for the exit), whatever step it is in; a step not reached is `CANNOT -- the bound`. The watch is active supervision: I read the guest's pidfile and the clock at most 60 s apart for the whole window (nothing alerts if the session disconnects), and the RETURN post names the stop.
- **Posts:** `START HH:MM:SS UTC` and `RETURN HH:MM:SS UTC` as the first lines on #673 and in the shared host log, each with the census (qemu live, compilers).
- **Every frame is labelled by side:** the image's EmulationStation is M7's composition over the pin, so a frame is `image` evidence unless the step's literal check shows the pin's lines unchanged there.

## The steps, in order

| Step | Proof | Image versus tree, first | What is read back |
| --- | --- | --- | --- |
| G01 | identity | -- | `BUILD_ID`, `BUILD_BRANCH`; `fbset` 640x480; the installed ES by two literals -- M7's `Pending achievements stay` and this pin's `USE CONNECT OR REPAIR CLOUD STORAGE` -- and the leads' own literals (`global.videofilters`, `ScrollLoadMedias`, `GAME MEDIAS DURING FAST SCROLLING`, `CLOUD CONNECTIONS`) by `strings | grep -c`; the hashes of `cloud_oauth`, `cloud_remote`, `setsettings.sh`, `001-functions`, `setrootpass` against `git show 8ebaf8daad:<path>` |
| G02 | L-02's reach | `cloud_oauth` (G01) | `cloud_oauth info`'s `ON_DEVICE` (no session started); `ls -l` of the sign-in window the script tests |
| G03 | L-10 (`ScrollLoadMedias`) | the label literal (G01) | UI SETTINGS: toggle GAME MEDIAS DURING FAST SCROLLING, close the page; `system.cfg` and `es_settings.cfg` before and after, read through the filter (`grep -v -i -E 'key|pass|token|user|psk'`) for that one key: the change lands in `system.cfg`, `es_settings.cfg` keeps `ScrollLoadMedias` as it was |
| G04 | L-09 (`global.videofilters`) | `setsettings.sh`, `001-functions` (G01) | GAME SETTINGS: the VIDEO FILTER row's frame (is it built and shown on this image?); if shown, a non-default choice, close; `system.cfg`'s `global.videofilters` and `global.videofilter` lines; `get_setting videofilter <a system>` from a login shell answers empty |
| G05 | L-11 (writes at open) | -- | `system.battery.warning_threshold` in `system.cfg` and `audio.useFavoriteMusic` in `es_settings.cfg` before and after opening SOUND SETTINGS and leaving it with no change |
| G06 | L-13 (the built unread rows) | -- | one frame each of GAME SETTINGS, FRONTEND DEVELOPER OPTIONS, SYSTEM SETTINGS, NETWORK SETTINGS at 640x480, scrolled: which of the eleven rows a player can reach on this image |
| G07 | the walks, EN | the literals (G01) | frames, strings read back: CLOUD (the hub), CLOUD CONNECTIONS, CONNECT CLOUD STORAGE and one provider's form, CLOUD STORAGE SETUP's wizard step 1 to the extent the guest allows (no SSH session is opened), CLOUD FOLDERS (the selection page), NETWORK SETTINGS, MANAGE SAVED NETWORKS; L-16: a 0.75 page's last row and both buttons on screen |
| G08 | the relink page and L-18 | -- | `touch /storage/.config/.restore-finish-pending` (the guest's own state); FINISH RESTORE PROCESS's frame; its CHECK CONNECTION with no cloud set up (the `rc 1` text, the frame); the marker removed after |
| G09 | back landings | -- | on CREATE FOLDERS (YES/NO) and one YES/NO in GAME SETTINGS' cloud rows: the frame after B on each |
| G10 | L-01 (the QR's cached read) | `cloud_oauth` (G01) | only if G02 shows a sign-in can start on this guest: `/tmp` remounted read-only for one sign-in attempt (text-only page), remounted, a second attempt in the same session: still text-only -- the positive; else `CANNOT` with the reason |
| G11 | the walks, FR | -- | `system.language=fr`, the G07 pages again, strings read back (L-19 and L-20 among them where reachable) |
| G12 | cleanup | -- | the guest stopped by its pidfile, the qcow2 removed with its path, size and sha recorded; `pgrep -x qemu-system-x86` reads 0 for the lane |

Steps G10 and G11 are the first dropped if the bound comes first; G01 to G05 are the ones the leads need.
