# Completed engineering artifact verification — #344 / #565 / #566 / #588

SOURCE ONLY; UNRUN. The active build is frozen at distribution d6a87f05c1935516115b2cca1af22151a0209224 and ES3178. This additive helper reuses the prior engineering artifact procedure and existing selected-state filesystem readers; it adds no release criteria. No image exists yet and no result is claimed.

Can this be done on the VM? Raw update/install container consistency and host build-output provenance use the host's existing read-only filesystem readers before boot. Runtime, clean/retained policy and behavior remain in the separately allocated guest. The helper never executes firmware binaries, mounts storage, edits a build input or contacts a provider.

After the build actually ends, read its original host/inner/runner/monitor/launcher results, verify actual owner/container exit, and consume admission. Then run this helper inside a fresh watched owner, with `--output` naming an existing empty private subdirectory. It requires those completed receipts and source/branch/identity bindings. It hashes the three actual engineering files before and after reading; validates both GPT header/table CRCs and two-partition geometry; compares raw-image and update-tar SYSTEM/KERNEL; compares selected final installation bytes/modes and complete proxy bytecode/controller-profile file sets with SYSTEM. Eight changed script mappings are also compared with the frozen source, using the package's exact GENERIC_X64 substitutions for the two Dolphin launchers; the save-path helper is included. It preserves SYSTEM/KERNEL and raw disk solely for the immediately following qualification. Do not treat this as clean-state policy or runtime acceptance.

The selected set also covers every installed #588 binder input: profile/functions, interpreter, controller/unit/autostart, systemd tools and declared native libraries. It compares every image-local symlink hop/target and resolved path, so the verified existing image/system tree can be reused as binder root without duplicating SYSTEM extraction. The actual flash syslinux.cfg is separately read from the install image with a30-second/64KiB bound for the binder.

The helper imports the exact existing `pixelelated-state-check` reader hash from the frozen checkout. Its Local/Squash readers resolve image-absolute symlinks within the image, never against the host. No full extracted filesystem or mode-000 shadow read is needed. The old build20 verifier's hardcoded wrapper-failure exception and old identities are not carried.

Execution uses one serialized host allocation after compilation: proposed 1500-second outer watchdog plus bounded cleanup, up to16GiB raw disk +4GiB SYSTEM +128MiB KERNEL +small records (reserve24GiB scratch). mcopy readers have180-second deadlines/output file ceilings, selected filesystem readers use their existing180-second limits and256MiB per-file ceiling. A final source-only syntax review is not a runtime acceptance. Preserve original results on failure; do not rerun into partial output.

```bash
# TASK_VERIFY_OWNER is a fresh admitted watched owner, TASK_OUTPUT its new empty evidence subdirectory.
python3 -I docs/qa-logs/2026-10-14-m7-image-verification/verify-image.py \
  --build-owner /workspace/tmp/pix-m7-engineering-build-20261014-01 \
  --output "$TASK_OUTPUT"
```

Then run the already sealed installed-state-plan/payload-check.sh once for each actual install/update payload, with its #566 positive shared-identity postcheck from the correction packet. These use independent private scratch; do not duplicate raw disks unnecessarily. Image-dependent #588 binding consumes the verified SYSTEM and actual final source/native/bytecompile/strip records, not a component ELF substituted into the image. Retire raw/scratch files after their immediate dependency ends; retain compact hashes, receipts and necessary corresponding-source inputs.

The source-only `prepare-readback.py` creates the fresh owner, exact verifier copy and retention/admission plans only after original build admission is consumed. Its command uses existing watch-build-submit, GNU timeout1500s/15s cleanup, one CPU and an explicit8GiB per-process address-space limit. It reserves24GiB scratch plus8GiB operating margin; no memory-controller claim is made. The preparer remains UNRUN until completed build receipts exist.

The pending installed-UI continuation also consumes actual browser/rclone/GStreamer inspection/scanner/GL/controller libraries and French/English catalogs. Their fixed installed paths are in the same byte/mode/link-chain comparison, before any accepted synthetic backend seam. The inspector still executes no target binary.
