# #1514: `tools/image-acceptance`, run on the round's handheld images

Can this be done on the VM? Yes, and no guest is needed. The tool reads a build's outputs on the host with `unsquashfs`, `sfdisk` and its own read-only FAT reader. It writes only its scratch, which it removes, and `--out`. The records here are the final runs, 2026-11-28 11:37:55 to 11:38:15 UTC (each file's first and last lines); `build27-H700-run1.txt` is an earlier run, before the tool printed its times.

## The runs

- **`build28-SM8550.txt`:** build 28 with `claims-6169621a4b.txt`, PASS, 82 checks:
  - the run's channels and processes;
  - checksums, `os-release`, identity, the worktree and the userland;
  - the ARM handoff: `retroarch32`, `box86`, two cores and all 181 `usr/lib32` files;
  - the GPT image's boot partition: SYSTEM, KERNEL, 14 DTBs, the loader entry and OpenABL, each equal to the tar's. The signed ABL is ELF32/EM_ARM;
  - the round's claims: #1501's strings, #1502's ctl, #1509's pin, #1459, #1422's UCM lines and #1448's FEX and log lines.
- **`build27-H700.txt`:** build 27, PASS, 97 checks.
  - The same common checks run here. The ARM handoff is skipped on purpose (`--skip arm-handoff`), because H700's ARM image went with its build root at SM8550's launch.
  - Both DDR images are checked: the MBR, the tar's DDR3 and DDR4 u-boot at byte 8192, and SYSTEM, KERNEL, 22 device trees and the DDR3 overlay on the boot partition.
  - Build 27's own acceptance had none of these raw checks.
- **The verdicts agree with the session scripts.** Both builds were accepted from `handheld-reads.sh`, `sm8550-extra-reads.sh` and `build28-raw-update.py`. The tool reads everything those did, and more on H700.

## What the tool's first runs found in itself

- **A FAT short name's case flags.** The reader first read `DTBS/` and `OPENABL/` where mtools shows `dtbs/` and `openabl/`, because it ignored the case bits in byte 12. The one check that would have shown this was then only a note. The tar-only list is now a check: every bootloader file of the tar must be on the boot partition, except the updater's `update.sh`, a raw-written u-boot, and the ATF it embeds. The reader's hash of the signed ABL equals the one mcopy gave (`2a2808d1…`, `build28/raw-update-28.json`).
- **H700's `bl31.bin`.** That check's first H700 run (`build27-H700-run1.txt`) failed on `bl31.bin`, which is in the tar and not on the partition. It is the ARM Trusted Firmware that H700's u-boot embeds: the device options' `ATF_BL31_BINARY`, an input to both u-boot recipes. Nothing copies it to the FAT. The tool now allows that name, read from the options. The FAIL showed the partition's contents beside the missing name, which is what made the cause a one-line lookup.

## Constructed failures (#1514 c2)

`claims-constructed.txt` writes the first pass's two wrong expectations as claims, plus a near-miss string. `constructed-SM8550.txt` shows each FAIL with what is there:

| Claim | Found |
| --- | --- |
| `log "\[DONE\] build fex-emu:host"` | `[701/732] [DONE] build   fex-emu:host` and the install line |
| `listed usr/bin/FEXInterpreter` | `usr/bin/FEX`, `FEXBash`, `FEXConfig`, …, nearest name first |
| `contains usr/bin/emulationstation "… RETROACHIEVEMENT SETUP"` | the nearest string, `SIGN IN AGAIN: GAME SETTINGS > RETROACHIEVEMENTS SETTINGS` |

## Not shown here

- **The tool's first use at a build's acceptance.** That is the next device build, and its acceptance record will list the tool's output.
- **A physical boot.** Nothing ran on a handheld.
