# Existing lawful native fixtures — source-only handoff

2026-10-14. All emulator execution, frames, input, SD creation and installed-image
qualification in this packet are **UNRUN**. Official downloads, hashes, DOL header
inspection and local helper syntax inspection are the completed work. This is an
internal fallback packet, not a Herdr lane. It does not gate engineering image
compilation on evidence that only the resulting image can supply.

Can this be done on the VM? **Yes.** Use the coordinator's installed GENERIC_X64
guest, disposable storage, no NIC/accounts, existing process owner and observation
tools. The live #575 criteria are retained in `issue575.json`. No new GameCube
memory-card or Wii NAND requirement is added to #581: its existing exact launcher
byte/type preservation evidence remains separate.

## Ready artifacts and scope

| Author artifact | Exact downloaded bytes | Intended observation | Limit |
|---|---:|---|---|
| SuDokuL v1.5 GameCube DOL | 4,973,812 | actual game, input, manual state, exit/return, frontend manager absence | saves through SD Gecko/SD2SP2, not a GC memory card; pinned Dolphin has no corresponding SD device |
| SuDokuL v1.5 Wii DOL | 6,204,908 | same, plus ordinary puzzle save/reload through emulated Wii SD | SD save does not prove Wii NAND or GC card writes |
| Demon Bazooka CDI | 1,806,697 | actual Flycast gameplay, manual state, native auto-state on orderly unload, frontend manager absence | no ordinary game progress save in inspected source |
| Dreamcast BASIC CDI | 1,958,537 | optional real VMU write/read diagnostic | saves a BASIC listing, not in-game progress; does not alone close that #575 observation |

`fixtures.json` binds every source commit, URL, length, download/member SHA256 and
scope. The two SuDokuL ZIPs total 5,631,052 bytes; the two Dreamcast CDIs total
3,765,234 bytes. Cached data is at
`/tmp/pix-m7-native-homebrew-20261014/payload/`. No SDK, proprietary BIOS, ROM
collection, source rebuild or container is needed for this proposed route.

Primary sources: [SuDokuL v1.5 release](https://github.com/Mode8fx/SuDokuL/releases/tag/v1.5)
and [source f5993339](https://github.com/Mode8fx/SuDokuL/tree/f5993339c0e245c3cf52a26ac614309b199eb8c6);
[Demon Bazooka source](https://github.com/richstokes/dreamcast-homebrew/tree/1eec70cd343704d1a277c1a2e9b653cddcfd3b3d/projects/games/demon-bazooka)
and [BASIC source](https://github.com/richstokes/dreamcast-homebrew/tree/1eec70cd343704d1a277c1a2e9b653cddcfd3b3d/projects/apps/dreamcast-basic).
SuDokuL original code is MIT (GateGuy); its release embeds music with in-game
credits. Rich Stokes's original code is MIT; KallistiOS and BASIC's font/example
attributions remain in the author documentation. Retained licenses/credits are in
`licenses/` (the GC readme uses normalized LF line endings; its original bytes remain in the hashed ZIP). These are author-distributed homebrew, not commercial game dumps.
The rolling Dreamcast release is pinned by full source SHA, release metadata and
asset digest, not by trusting the mutable `continuous` label. Binary reproducible
build equivalence has not been claimed. `materialize.py` refuses changed bytes.

## Exact next preparation command

From this packet directory (data preparation only, no runtime):

```sh
python3 materialize.py \
  --cache /tmp/pix-m7-native-homebrew-20261014/payload \
  --out /tmp/pix-m7-native-homebrew-staged-01
```

The output must not exist. `--download` is an explicit fallback for absent cached
files and permits only bounded, hash-checked URLs from the manifest. Keep the
license folder beside any transferred fixture staging bundle. Stage those exact
files through the coordinator's existing offline guest transfer mechanism:

```
SuDokuL-GC.dol       -> /storage/roms/gamecube/SuDokuL-GC.dol
SuDokuL-Wii.dol      -> /storage/roms/wii/SuDokuL-Wii.dol
demon-bazooka.cdi    -> /storage/roms/dreamcast/demon-bazooka.cdi
dreamcast-basic.cdi  -> /storage/roms/dreamcast/dreamcast-basic.cdi
```

Both Nintendo system declarations already include `.dol`; Dreamcast includes
`.cdi`. No product XML change is required. Require installed image SHA, installed
ES/engine/launcher hashes and the effective system/game emulator/core/settings
receipt before observing behavior. Record global autosave independently of native
options. Keep retained-state checks on a separate disposable storage clone.

## Dolphin sequence

Use the installed `runemu.sh` route. `bash native-launch.sh gc` and
`bash native-launch.sh wii` provide exact hash-checked launcher commands; `gc-qt`
and `wii-qt` are available only where the existing acceptance flow needs Qt.
Normal ES game-page launch with these selected cores supplies the frontend and
time-to-play proof; a direct helper launch alone does not prove ES return/selection.
Bind the actual controller mapping rather than assuming host keyboard defaults.
The Wii game also reads the GameCube controller, so the same mapped GC pad on
port 1 can drive both cases. Preserve launcher-generated profiles.

1. Frame the game title, start a puzzle, then frame its actual grid. Fresh settings
   use A to confirm, B to go back, D-pad to move, Start to pause and Z to choose
   the pause screen's Save and Quit. Retained settings may swap A/B; bind them.
   Make one visible editable-cell change and record coordinates/value. A title
   frame alone is not gameplay; a moving cursor alone is not save persistence.
2. Select slot 1 explicitly and observe its on-screen selection. Use the shipped
   native save hotkey, change the visible puzzle/cursor, then use the load hotkey
   and observe restoration. Record actual created state paths and SHA/times before
   and after. DOL naming may use the fallback game ID, not `SuDokuL.s01`. The Qt
   template loads slot 1 specifically, so do not assume slot 0 or another slot.
3. With global automatic states off, then on, exit through the installed native
   exit route. Capture original engine/launcher exits, final state-file inventory,
   ES return frame and next first frame. Preserve the distinction between no
   automatic state creation and an existing manual state left unchanged.
4. Frame the game page's manager/action availability with standalone selected.
   The existing manager is RetroArch-only; a native state file does not imply
   frontend manager support. Account/RA title identification is outside this test.

For Wii ordinary save, prepare a **fresh 128 MiB SD image**, only after allocation:

```sh
bash prepare-wii-sd.sh /tmp/pix-m7-sudokul-sd-01.raw
```

This needs host `mtools`, creates a FAT image with `/apps/SuDokuL`, and never mounts
it. Transfer it to `/storage/qa-m7-homebrew/sd.raw`. Seed the guest's normal Dolphin
config through its installed setup/launcher first, while retaining that stage's
original exit. When the engine is stopped, record the exact existing INI hash and:

```sh
python3 configure-wii-sd.py /storage/.config/dolphin-emu/Dolphin.ini \
  /storage/qa-m7-homebrew/sd.raw --expected-ini-sha256 RECORDED_INI_SHA256
bash native-launch.sh wii
```

The helper saves the original INI once and sets the pinned Dolphin's Core
`WiiSDCard`, `WiiSDCardAllowWrites`, `WiiSDCardEnableFolderSync` and General
`WiiSDCardPath`. In the game, change a cell, Start then Z (Save and Quit), exit the
engine cleanly, and retain the quiescent SD image. On its host copy:

```sh
mdir -i /tmp/pix-m7-sudokul-sd-after.raw ::/apps/SuDokuL
mcopy -i /tmp/pix-m7-sudokul-sd-after.raw ::/apps/SuDokuL/save.bin /tmp/pix-m7-save-after.bin
sha256sum /tmp/pix-m7-save-after.bin
```

Relaunch **without loading a native state**, choose Play/Continue and require the
same saved cell/puzzle. Source `savePuzzle()` silently skips a failed file open,
so menu navigation alone is insufficient. Keep a baseline image, original
`settings.bin` and before/after bytes. This is a real ordinary game save on SD.
For GC, record ordinary save as unsupported by this fixture's SD device path;
do not fabricate a successful card/NAND proof or add an SDK project as a gate.

## Flycast selection and practical next test

GENERIC_X64 already selects `flycast-sa` in virtual/emulators. Dreamcast defaults
to RetroArch/flycast; explicitly select **flycast / flycast-sa** for this case.
The accepted replacement20 image root already contains a 31,959,608-byte
`/usr/bin/flycast`, SHA256
`a54346440e53a42b477ce93752c532c8fb69a8bd16355c4d0f5e787141ba308f`.
This is a parent-cache fact, not final image proof. See the exact inventory JSON.
Select OpenGL through the existing graphics-backend setting for the QA VM and
record resulting `pvr.rend = 0`; the recipe can choose Vulkan by default.
Use built-in HLE BIOS for this homebrew; do not acquire proprietary BIOS files.

`bash native-launch.sh flycast-game` runs Demon Bazooka through the real launcher.
A/Start begins, D-pad/analog moves, A fires, B dashes. Frame first interactive
play, change position/score, save manually through Flycast's own menu, change the
scene and load. Observe the native state file and restored scene. Its entirely
code-generated game content requires no external assets.

Run native AutoSaveState/AutoLoadState off with ES global 0 then 1; then native
options on with ES global 0. Use Flycast's **orderly stop/unload** to test native
automatic states and relaunch to observe restoration. Separately exercise the
shipped exit route and record what actually happens: `start_flycast.sh` installs
`set_kill set "-9 flycast"`. A SIGKILL result cannot be called orderly unload or
assumed to flush native automatic state. Preserve original failure/result codes.
Frame absent ES manager independently. No integration change is proposed here.

Optional VMU diagnosis: `bash native-launch.sh flycast-vmu-diagnostic`. In the
disposable Flycast config, retain controller+VMU on port A and map a keyboard to
port B (`[input] device2=5`, `maple_sdl_keyboard=1`), as the author's runner does.
Type `10 PRINT "M7 VMU"`, F6 save as `M7QA`, exit cleanly, retain VMU image bytes,
relaunch and F7 load `M7QA`, F5 run. Source calls real KOS VMU `fs_open`, `fs_write`,
`fs_vmu_set_header` and `fs_close`; require the observed listing/output and a changed
VMU image. This establishes native VMU application persistence only. A small
lawful game with an actual progress/high-score save remains the precise missing
Flycast fixture for #575's in-game-save wording. No such accepted cached fixture
was identified in the inspected QA packets; no owner game library was scanned.

## Existing evidence and bounded allocation

Reuse `tools/emulator-exit-test --vm` on the admitted guest through its existing
runner: its self-authored ExitProbe.gb writes 0x55 to battery-backed RAM, and the
suite checks the actual RetroArch save and exit path. It is an engine/save probe,
not interactive game evidence. #196's historical 2026-09-15 ledger records real
manual-slot load and auto-state exit behavior; current-image manual/auto/manager
observations still need the ordinary image qualification. Do not relabel old
image receipts as final-image proof. Recent #575 UI fixtures prove capability
presentation, and #581 recording-engine fixtures prove preservation; neither
proves native gameplay or ordinary writes by Dolphin/Flycast.

Proposed first allocation: reuse one existing 4-vCPU/8-GiB installed-image QA
guest, one engine at a time, 30-minute wall budget for the initial qualification
session, first interactive-frame bound 120 seconds per launch, 128 MiB SD plus
before/after copies, at most 512 MiB new payload/state evidence. These are harness
bounds, not modified engine timers. Stop the stage on a failed observation and
keep original exits, frames, disk inventory and owner result. Do not force a PASS
by shortening waits or treating cleanup termination as the original result.
Confirm engine child and input-helper owners are gone and ES has returned.

Outstanding facts: installed new-image engine closure/hashes, actual display and
pad mapping, Wii SD mount/save success, each native manual/exit/manager result,
and a lawful Flycast in-game-save fixture. These belong to image qualification,
not admission to the current engineering build. No claim in this packet closes
#575, #581, a native gameplay criterion or an RC acceptance item.
