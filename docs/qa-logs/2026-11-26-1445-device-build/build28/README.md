# Build 28: SM8550 from the round's final head 6169621a4b (route 16)

- **Run:** `m7-round-sm8550-20261128/.build-runs/20261128T064843Z-a7b15e8b`, cold, owner `m7-round-sm8550-20261128-02-owner`. It ran 06:48:43 to 10:47:41 UTC with build.rc 0 and [732/732] packages. The runner, the command and the monitor each returned 0 (`runner-result.json`).
- **Before it:** the 06:27 launch was refused because a reader held H700's `.ccache` (#1512). Five proofs of #1510 and #1512 passed first, then this launch (`docs/qa-logs/2026-11-28-device-build-1510-1512/`).
- **Accepted:** `ACCEPTANCE-28.json`, admission `ad5f72d56cf2492f997f3e0d2e1ce351` consumed at 10:54 UTC. The build roots and `target/` stay held as the warm base (D-INFRA-037).
- **The common reads,** in `image-reads-28.txt` and `duck-28.txt`:
  - the image and the update tar check out against their checksums;
  - BUILD_ID is the head, with no `.dirty`, and the worktree is clean;
  - the ES binary carries the sign-in-again and wait sentences, and the French catalog carries the #1501 line;
  - `raofflineproxy-ctl` equals the round's source;
  - `/usr/bin/duckstation-sa` hashes to the aarch64 pin `f92319a0…` (#1509).
- **The SM8550-only reads,** in `image-reads-SM8550-extra.txt` (from `sm8550-extra-reads.sh`):
  - **#1459:** the SYSTEM listing has no `usr/share/aethersx2-sa/aethersx2`. The bring-your-own recipe still ships its start scripts, config and `GameIndex.yaml`, and those are listed in full.
  - **#1422:** the installed `HeadphoneEnableSeq.conf`, `Retroid/Nova/HeadphoneMode.conf` and `AYN/Odin2/AYN-Odin2.conf` carry ROCKNIX #3481's Nova Class-AB headphone quirk. What comes out of the Nova's jack stays an open item to test.
  - **#1448:** fex-emu is built for host (`[701/732]`) and target (`[724/732]`). `usr/bin/FEX` and both binfmt confs ship. Fifteen listing entries name GuestThunks, 8 of them files under `usr/share/fex-emu/GuestThunks/`.
- **The raw/update acceptance (#555's SM8550 checkbox),** in `raw-update-28.console` and `raw-update-28.json`, from `build28-raw-update.py`. It follows the October reader `2026-10-11-device-refresh/sm855005/prepared/acceptance05/verify-firmware.py`, with OpenABL's folder `openabl/` in place of `rocknix_abl/`. Every check passes:
  - both outputs match their `.sha256`;
  - the raw image is a GPT with 512-byte sectors and two partitions, `system` from sector 32768 and `storage`;
  - the boot partition's SYSTEM and KERNEL equal the update tar's;
  - OpenABL 1.2's signed ABL (`PKG_VERSION="1.2"`) is ELF32/LE/EM_ARM, sha256 `2a2808d1…`. It and its three scripts are equal in the tar, in the SYSTEM's `usr/share/bootloader/openabl/` and on the boot partition;
  - all 20 boot files except `update.sh` are on the boot partition, byte for byte;
  - os-release names `pixelelated`, the head, `build/m7-round-sm8550-20261128`, `BUILD_DIRTY=no`, SM8550 and aarch64, and `identity.json` agrees;
  - ES, RetroArch and FEX are ELF64 AArch64;
  - the ARM handoff holds: `retroarch32`, `box86`, gpsp and desmume are 32-bit ARM and equal to this run's ARM image, and so are all 181 of its top-level `usr/lib` files in `usr/lib32`.
  - It is a later read than `ACCEPTANCE-28.json`, which was consumed first, so it is kept beside that record and not listed in it.
- **The first run of the extra reads failed on two of its own checks,** kept as `image-reads-SM8550-extra-run1.txt`:
  - the build log writes `[DONE] build   fex-emu:host` with padding, and the check expected one space;
  - this FEX installs its interpreter as `usr/bin/FEX`, the name #1448's earlier tick already cited, and the check asked for `FEXInterpreter`.

  The image did not change between the runs. The corrected checks match the log and the package's `install_pkg/`.
- **The log's paths name `conflict-resolution/.build-runs/m7-candidate-build-20261118-01/checkout`.** That is the container's `DOCKER_WORK_DIR`, kept so the warm caches' generated paths resolve (`admission.json`'s `container_checkout`).
- **The patch replay for this head** ran at the first, refused launch (06:25–06:26 UTC, owner `m7-round-sm8550-20261128-owner`). Every patch applies: 167 packages each, 517 applications for aarch64 and 510 for arm (`replay-aarch64.console`, `replay-arm.console`). The set file records it per head and device, so the `-02` launch did not repeat it.
- **Not a device qualification.** Nothing has been staged on a handheld.
