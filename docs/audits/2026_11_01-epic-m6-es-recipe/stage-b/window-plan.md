# T37 (#684): the guest window's plan (stage B)

The brief's § 5 item 2, with stage A's and stage B's adjustments named. **Nothing runs before the
coordinator's grant on #684 and its line in `/workspace/tmp/m7-m6-host-coordination.txt`.**

- **Can this be done on the VM?** Yes, for what the installed image shows. No image of the tip's
  recipe exists (nothing builds in this slice), so every row reads what the M7 candidate installed,
  labelled by side: `ui-equal` where the installed file comes from a `ui/` file byte-identical in
  the candidate's tree and the tip's (read as the tip's), `candidate` where it comes from the
  candidate's own recipe or ES (read as what the M7 line shipped, never as the tip's behaviour;
  ruling (h)). What only a build shows -- a stamp, the `USING:` lines, the gettext pass, the CMake
  cache, the H700 and SM8550 branches, upstream's RK3566 patch -- is `CANNOT` and the integration's.

## The request

- **The guest:** one GENERIC_X64 guest from M6's copy of the candidate,
  `/workspace/artifacts/m6-t2-20261023/pixelelated-GENERIC_X64.x86_64-0.0.1-dev+20261022T235948Z.g069fc2704421-from-ROCKNIX.img.gz`
  (2,122,289,964 bytes; sha256 `6b4c3079bdee2f47bd1149aac07b11714c591b847f22157fcd6d85f39a7e08fb`,
  equal to its `.sha256` at stage B, `state-check-host.out`), on **a fresh disk** of the lane's own
  under `/workspace/tmp/m6-t37/guest/`: `gunzip -c` to `disk.img`, `qemu-img convert -O qcow2`,
  `qemu-img resize` to `16G`. **Never `t2.qcow2`** beside the image.
- **One boot at 640x480:** `projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm run --headless
  --daemonize --res 640x480 --pidfile /workspace/tmp/m6-t37/guest/qemu.pid --serial
  /workspace/tmp/m6-t37/guest/serial.sock <qcow2>` (#1141), isolated from the network as T36's
  window was (`restrict=on`, no `guestfwd`) in the form the grant names. No second boot.
- **Bound: 15 minutes proposed, plus 5 of grace, from the START post.** The plan is G-01 to G-07
  at 780 s (13 min): `printf '%s\n' 60 120 120 180 120 60 120 | awk '{s+=$1} END {print s}'`
  printed `780` (the brief's R5 C14; re-run at stage B, `780`).
- **The stop:** a detached timer started with the guest, `setsid` and `nohup`, that runs `tools/vm-stop
  /workspace/tmp/m6-t37/guest/qemu.pid <qcow2>` at bound plus grace (20 minutes after START); its
  PID goes in the START post and line. The normal stop is G-07's `tools/vm-stop` on the pidfile,
  never a pattern, and the timer is then stopped by its own PID.
- **The image identified by two literals first:** `BUILD_ID` from `/etc/os-release` and the file
  name (G-01).
- **The posts:** `START HH:MM:SS UTC` / `RETURN HH:MM:SS UTC` open each post on #684 and the
  matching host-file line, each with the census (`qemu N, compilers N`).
- **Before the guest:** the host file read whole; **the START waits for any open M7 standing or
  compile START's RETURN (#1293)** and for T36's slot; the guarded `tools/build-preflight
  --reclaim-swap` at most once, before the guest, never beside it.
- **Every read** goes over `tools/vm-serial sh` through the device read filter (`grep -v -i -E
  'key|pass|token|user|psk'`), or the masking `sed` of `engineering-practices.md` where the line's
  presence is the evidence. G-05's string counts are counts only.
- **The guest writes nothing**: no file, no setting, no stamp; no reboot after first boot; no game,
  no cloud, no QA account, no hosted account; the owner's accounts never (D-QA-015).
- **After:** the disk and its `disk.img` retired with path, size and sha (D-INFRA-022), recorded in
  `00`; the leftover check `qemu 0, compilers 0`; the window closed inside its bound plus grace.

## The rows

| G | What only the installed image shows | Serial command (over `tools/vm-serial sh`, filtered) | Expected line | Side | Bound (s) |
| --- | --- | --- | --- | --- | ---: |
| G-01 | identity; the binary | the file name by `ls -l` on the host; `grep -E '^(BUILD_ID\|BUILD_BRANCH\|BUILD_VERSION)=' /etc/os-release`; `sha256sum /usr/bin/emulationstation` | `BUILD_ID="069fc270442134fe771258418adf4e666e0473fb"`, `BUILD_BRANCH="build/m7-signin-20261022-07"`; the binary `25155163fd7970f7da54b3f36d003b8c006111c894d4fe6f0c92d24d51831226` (R3 G1, G2). **The `ldd` line is not repeated**: T36's G-01 on this image holds it (`libfreetype.so.6` and `libvlc.so.5` linked, `libfribidi` NOT linked; T36's `00:54` at `775d0893fe`), cited (R5 § A) | candidate | 60 |
| G-02 | the themes installed, the default, and L-22's font | `ls /usr/share/themes/`; in `es-theme-art-book-next/`: `ls pixelelated-wordmark.svg Tiny5-OFL.txt`, `ls -d _inc/systems/artwork-*`, `grep -c -E 'include name="(noir\|nintendont\|circuit\|outline)"' theme.xml`, `grep -c 'lang="zh"' fonts.xml`, a line each fork patch adds; `ls -l _inc/fonts/`; **`ls -l /usr/share/fonts/truetype/noto-cjk/NotoSansCJKsc-Regular.otf`** (L-22); `readlink /etc/emulationstation/themes`; `cat /usr/config/emulationstation/es_settings.cfg`; `grep -i theme /storage/.config/emulationstation/es_settings.cfg` | the two fork files present; the five removed sets absent (`:19`); `0` (`:20`); `>= 1` (`:21-27`); both patches' lines present; the four bundled fonts; **the noto-cjk file present** (`candidate`: it is `noto-sans-cjk`'s); `/storage/.config/emulationstation/themes` (`:100`); the empty `<config>`; the default the image chose (L-20) | ui-equal (the font file: candidate) | 120 |
| G-03 | the configs, the link, the catalog and the locale | `sha256sum /usr/config/emulationstation/*.cfg` against `git show 2174265e9c:<path> \| sha256sum` on the host; `grep -c -i vulkan /usr/config/emulationstation/es_features.cfg`; `readlink /etc/emulationstation/es_systems.cfg` then `test -e /etc/emulationstation/es_systems.cfg; echo "resolves rc=$?"`; `stat -c '%a %n' /usr/config/emulationstation/*.cfg`; `ls -l /usr/config/locale/fr/LC_MESSAGES/emulationstation2.mo`; `readlink /usr/share/locale /usr/lib/locale`; `ls -d /usr/config/locale/en_US.UTF-8` | the four cfg digests equal to the tree's (`VULKAN_SUPPORT=yes` on GENERIC_X64, so `:126-128` did not run); vulkan `> 0` (`15` in the tree, R19); the candidate's `/usr/config/...` link, resolving (L-03); the seeds' modes (#1193); the catalog present (L-08); `/storage/.config/locale` (`:134`); the pre-generated locale present (L-07) | the cfgs ui-equal; the link candidate | 120 |
| G-04 | the services, the start and boot to interface | `systemctl show -p ActiveState,FragmentPath essway.service emustation.service`; `systemctl cat essway.service`; the `.wants` links; `sha256sum /usr/bin/start_es.sh /usr/bin/es_settings /usr/bin/serial_number_check` against the tree's on the host; `ls -l /var/log/es_log.txt`; the running ES's `cmdline` through the masking `sed`; `journalctl -b` for the interface's start, filtered | the fork's three lines in `essway.service`; the three digests equal to the tree's; **`--log-path /var/log` passed and `/var/log/es_log.txt` written** (PL-029: the flag inert, `Paths.cpp:81` the path); boot to interface in seconds, the guest's (time to play) | ui-equal | 180 |
| G-05 | the sources, the binary's strings and the resources | `head -n 5 /usr/bin/es_settings /usr/bin/serial_number_check` (read, never run); `strings /usr/bin/emulationstation \| grep -c -E 'SCREENSCRAPER_DEV_LOGIN\|SCREENSCRAPER_RUNTIME_DEV_LOGIN\|GAMESDB_APIKEY\|CHEEVOS_DEV_LOGIN\|HFS_DEV_LOGIN'`; `strings /usr/bin/emulationstation \| grep -c 100-amd64-freqfunctions`; `ls -l /usr/config/emulationstation/resources/logo.png`; `readlink /usr/config/emulationstation/resources/DroidSansFallbackFull.ttf` and `test -e` of it | counts only: the names `0`; `0` for the patch's string (L-02); `logo.png` present (L-04); the noto-cjk target, resolving. **The state check on the guest is `CANNOT -- the tool is not on the image and the window writes nothing`** (the coordinator's answer 2); its host half ran at stage B (`state-check-root.out`: `status pass`, 279 checks, 278 `clear`, 1 `allowed`: `/usr/bin/emulationstation approved-shared-developer-identity`) | candidate | 120 |
| G-06 | `lowerdeck` on GENERIC_X64 | `ls /usr/share/lowerdeck` | present (`PKG_UI`, `BASE_ONLY` empty) | ui-equal | 60 |
| G-07 | close | `tools/vm-stop` on the pidfile; the timer stopped by its PID; the disk's size and sha; `qemu 0, compilers 0` | `retired.txt`; the leftover check; the RETURN post inside bound plus grace | -- | 120 |

Sum of the bounds: `780`. **The guest writes nothing** -- no row writes a file, a setting or a
stamp.
