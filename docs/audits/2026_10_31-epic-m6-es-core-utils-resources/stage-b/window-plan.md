# T36 (#683): the guest window's plan (stage B)

This plan is the brief's § 5 item 2 and its G table, in T35's request shape (the coordinator's `kit/t35-vm.txt`). Nothing runs before the coordinator's grant on #683 and its line in `/workspace/tmp/m7-m6-host-coordination.txt`.

- **Can this be done on the VM?** Yes. The host first (stage C's cases), then this one guest window. G-08 and G-09 are `CANNOT` by structure and by device; ES's VRAM counters in G-05 are `CANNOT` (no tool reads them).

## The request

- **The guest:** one GENERIC_X64 guest from M6's `069fc2704421` copy of the image at `/workspace/artifacts/m6-t2-20261023/`.
  - The file is `pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`, 2,122,289,964 bytes (the lane's `ls -l` at stage B).
  - It boots on a fresh qcow2 of the lane's own under `/workspace/tmp/m6-t36/`, headless and daemonized. T2's `t2.qcow2` beside the image is not used.
- **Two boots on the same disk:**
  - First at 640x480: `generic-x64-vm run --headless --daemonize --res 640x480` (#1141).
  - Then for G-06, stopped by pidfile (`tools/vm-stop`) and started again at 1280x800. `fontScale()` is 1.31 under 720 px and 1 at 1280x800 (R3 § 4), so the font's scaling shows only at both sizes.
- **Bound:** 25 minutes proposed, plus 5 of grace, from the START post.
  - The plan is G-01 to G-10 at 1,080 s (18 min), by the lane's own command `printf '%s\n' 60 120 180 240 120 180 60 0 0 120 | awk '{s+=$1} END {print s}'` (`1080`). The second boot is inside it.
  - For comparison: T35's window was 30 + 5 for 26 minutes, T34's 30 + 5 for 23.5, and T33's 25 + 5 for 21.
- **The image identified by two literals first:** `BUILD_ID` from `/etc/os-release` and the file name (G-01).
  - **Labelled by side:** every verdict is labelled `image`, or `pin-binary` only where the digest found the pin's lines unchanged in the image's binary. The image's EmulationStation is M7's composition.
- **The posts:**
  - `START HH:MM:SS UTC` and `RETURN HH:MM:SS UTC` open each post on #683 and the matching line in the host file, each with the census (`qemu N, compilers N`).
  - **The START names the detached timer that stops the guest at bound plus grace, with its PID, or says that nothing does** (`engineering-practices.md`, #1135).
  - **The stop is by pidfile** (`tools/vm-stop`), never by pattern.
- **Before the guest:** the guarded `tools/build-preflight --reclaim-swap` is allowed once, never beside the guest. The host file is read whole before the START, and **the START waits for any open M7 #1293 START's RETURN.**
- **Named in the START post:**
  - **G-03:** the page is the game list's detailed view of a game whose MANUAL row is decided from the cached `exists` (`DetailedContainer.cpp:899-916`, #1263's page). The path is that game's manual file, written over `tools/vm-serial` after the list was shown. The system and the file name are taken from G-01's listing of the guest's ROMs.
  - **G-04:** the page is the same view's play-time field (`DetailedContainer.cpp:1049`, `Utils::Time::secondsToString`, `TimeUtil.cpp:514-588`). Its game's `<gametime>` is set over serial with ES stopped, so that each threshold string is drawn.
- **After:**
  - The disk is retired with its path, size and sha (D-INFRA-022), recorded in `00`.
  - The leftover check reads `qemu 0, compilers 0`, and the window closes inside its bound plus grace (G-10).
  - Nothing changes but the guest's own files.
- **Never:**
  - the owner's accounts (D-QA-015);
  - the QA accounts, which no row needs (`tools/qa-accounts`, never printed);
  - any hosted account, sign-in or provider;
  - anything of the three holds on the guest unless the coordinator asks for it in the grant. Their cases run on the host at stage C, with their output held.

## The rows

| G | Behaviour only the running image shows | Walk or serial command | Expected frame or line | Bound (s) |
| --- | --- | --- | --- | ---: |
| G-01 | identity; the face, the theme, the libraries, the renderer | `vm-serial sh` over `cat /etc/os-release; fbset; ls /usr/share/themes; find /usr/share -name "*.ttf" \| head; ldd /usr/bin/emulationstation \| grep -E "fribidi\|vlc\|freetype"`; the theme's XML grepped for a `fontPath` without a `fontSize` (L-07's reach); the ES binary's digest against the pin's lines; `vm-qa`'s renderer line; the guest's ROM listing for G-03 and G-04 | `BUILD_ID=...`, `640x480`; the face path for `tools/font-stems`; whether `libfribidi` is linked (Q7's `HAVE_FRIBIDI`); L-07's element present or absent; Mesa's virgl line | 60 |
| G-02 | the font's scale at 640x480 (`Font.cpp:99-101`, `:161-180`; `Renderer.cpp:1149`) | the carousel and one menu page with a help bar; `shot` each | the help bar's height and a row's text height measured by a stdlib `zlib` PNG reader against T34's 70/71 px and `tools/font-stems`' stems -- `image` | 120 |
| G-03 | the `exists` cache after a file written by another process (`FileSystemUtil.cpp:213-215`, `:277-282`) | ES running; the page named in START opened; the file written over serial; the page left and reopened; `shot` before and after | the row's two frames: the remembered miss shown, or the file seen; 3.13, 3.26 and T35's 3.11 are the proof, the frame the confirmation -- `image` | 180 |
| G-04 | the 11 strings in English and French (`TimeUtil.cpp:517-588`; `MathExpr.cpp:95`) | the page named in START; `shot`; `systemctl stop essway`; `system.language` set to `fr_FR` over serial; ES started; the same page; `shot` | each duration string drawn at 640 in both languages without clipping, the French the catalog's (`jamais`, `%d j`, `%d h`, `%d mn`, `%d sec`) -- `image` | 240 |
| G-05 | the renderer through Mesa virgl (`Renderer_GLES30.cpp`; the texture cache under a scroll) | `vm-qa`'s display and renderer lines; a game list with art scrolled its length; `tools/es-launch-memory` before and after | frames without a missing texture or a torn clip; RSS before and after; **ES's VRAM counters `CANNOT`** -- `image` | 120 |
| G-06 | the second size: the font's scale at 1280x800 | `tools/vm-stop`; `generic-x64-vm run --headless --daemonize --res 1280x800` on the same disk; `vm-serial wait`; G-02's page again; `shot` | the same measures at `fontScale()` 1 against T34's 118/118 px; the two sizes' ratio as the reader's line -- `image` | 180 |
| G-07 | the launch's SIGPIPE disposition, the pipe under the image's shell, the image's launch wrapper (`Platform.cpp:162-168`; L-05) | **first** `grep SigIgn /proc/$(pidof emulationstation)/status` (bit `0x1000`); then the brief's loop over `seq 1 400` and `seq 1 200000` under `sh -c`, and `readlink -f $(command -v sh)`; the image's `runemu.sh` with `grep -n -E 'LOG_FILE=\|OUTPUT_LOG\|tee -a'` against the source's `:40`, `:46`, `:84`, `:491`, `:500` | `SigIgn`'s bit as it prints; the two exits the image's shell prints, as they print (the host's dash: `0`, `141`); the shell's path; the wrapper's lines or the difference named -- `image` | 60 |
| G-08 | `Renderer_GL21`, `Renderer_GLES10`, `Renderer_GLES20` | -- | `CANNOT`: no image compiles their bodies (`-DGLES3=1`); a structure fact in `02` | 0 |
| G-09 | the handhelds' GL drivers (panfrost on H700, Adreno on SM8550) | -- | `CANNOT`: a device no (`vm-first.md`); a driver-specific defect is an `open item to test` with the physical fact named | 0 |
| G-10 | close | `tools/vm-stop` on the pidfile; the disk's size and sha; `qemu 0, compilers 0` | `retired.txt`; the leftover check; the RETURN post inside bound plus grace | 120 |

Every frame is read back for its strings, and every measurement in pixels is made by a reader, not by eye. A fix's frame is `fix-walk-pending-image`.
