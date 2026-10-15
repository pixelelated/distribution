# Next-image readback verifier — #584 / #592, SOURCE ONLY

This is a small derivative of the ACTUAL qualified verifier at /workspace/tmp/pix-m7-image-readback-20261014-02, including its exact verify-image.py, run.sh, inputs and original completion/consumption receipts under originals/. This packet has never been executed or imported. No preparer, worktree, admission, compiler, container, image reader, VM, fixture or service ran during preparation. No shared product source or prior owner changed.

The future build owner is /workspace/tmp/pix-m7-engineering-build-20261015-01; expected checkout/branch are m7-p5-build-20261015-01 and build/m7-p5-20261015-01. Final source/time/output bytes do not exist in this plan. inputs.template.json deliberately leaves source/build_run null. At execution, verify-image.py requires actual completed build-inputs/owner/resources/launcher/runner/admission-consumed records and exited original owner/container identities, checks exactly clean-dolphin-sa → build-dolphin-sa → image, and derives the actual source, timestamp, image name and artifact hashes. It checks final reviewed product hashes from the build owner and unchanged Dolphin pin6094cfcf7b8fba733b3116fdf3414d51c1c0e4a4. It cannot turn a preparation file or unfinished build into readback acceptance.

## Six added selected product mappings

The required alias is /usr/share/dolphin-emu/sys → ../../config/dolphin-emu. The four PNGs, ApprovedInis.json and GMSE01.ini below are bound to the exact pinned Data/Sys source, not merely equality between two installed copies.

| Suffix below usr/share/dolphin-emu/sys/ | Bytes |
| --- | ---: |
| Resources/achievements_player.png | 1164 |
| Resources/achievements_game.png | 1234 |
| Resources/achievements_unlocked.png | 583 |
| Resources/achievements_locked.png | 560 |
| ApprovedInis.json | 31627 |
| GameSettings/GMSE01.ini | 3737 |

The sealed dolphin-sys-source-manifest.json records each full SHA256, exact git blob, git mode100644, source-relative path, installed path and resolved target. During source preparation, all38905 bytes in the frozen unpacked tree were independently compared with git show at the exact Dolphin pin; every file matched. During future verification, each NEW built source file must still match that manifest, and normal source_mappings compares it against staged installation. The existing products loop compares staged installation versus extracted SYSTEM bytes, mode and complete link_chain. The added checks require mode -rw-r--r-- and exactly:

```json
{
  "resolved": "/usr/config/dolphin-emu/<suffix>",
  "links": [
    {"path": "/usr/share/dolphin-emu/sys", "target": "../../config/dolphin-emu"}
  ]
}
```

Each of the six rows appears in result.json products with the existing bytes/sha256/mode/link_chain schema, so frame_diff_review can require them directly before its independent installed guest checks. result.json and inputs.json also bind the source-manifest hash. source_mappings includes the exact source-relative files in the new completed Dolphin package tree. The record does not claim that runtime consumed a resource; the installed agent owns that acceptance.

## Preserved checks and limits

No existing digest, record, git, process_gone, copy_bounded, gpt or link_chain helper changed. The exact-hash existing pixelelated-state-check Local/Squash reader remains unchanged. There is no new reader or generic framework.

All original completed-source/branch/build identity checks, owner/launcher/runner and consumed-admission checks, per-stage inner/wrapper/container absence checks, raw disk bounds, primary/backup GPT CRC checks, normal install bootloader readback, raw/update SYSTEM and KERNEL byte equality, existing selected ELF/script/library/catalog/profile mappings, symlink-chain/mode comparisons, os-release fields and final artifact rehash remain. No failed original status is converted to success. The only branch replacement fixes the new expected build branch; the new exact-stage assertion adds the three Dolphin stage names.

run.sh retains exec semantics and the original CPU0,8GiB process address-space ceiling,16GiB per-file limit,1500-second work timeout plus15-second kill grace. It resolves verify-image.py beside itself and fixes the actual future build/output owner paths; it does not guess an artifact filename. The existing readback allocation retains24GiB payload/record allowance plus8GiB margin and the raw16GiB/SYSTEM4GiB/KERNEL128MiB ceilings. No additional proof matrix is introduced.

## Coordinator handoff after completed build

Root owns future materialization/admission/execution. This packet adds no preparer script. Use the existing qualified readback owner workflow, with these exact substitutions:

- Source packet: this assigned durable directory or a byte/mode-identical copy.
- Build owner: /workspace/tmp/pix-m7-engineering-build-20261015-01, after all original channels succeed and its admission is consumed.
- Fresh readback owner: /workspace/tmp/pix-m7-image-readback-20261015-01. Refuse an existing owner; create its fresh empty artifacts/ and empty-scan/ only when allocated.
- Copy verify-image.py, run.sh and dolphin-sys-source-manifest.json together; preserve source SHA256 and modes. run.sh works beside the source files in either the source packet or materialized owner.
- Materialize inputs.json from inputs.template.json using the real completed build-inputs.json SHA256/source/build timestamp and actual run.path. Preserve the original template; do not invent missing fields or edit original build results. The verifier independently checks the originals again.
- Use the unchanged original retention/admission formats under originals/: replace old checkout/owner/artifacts paths, bind the new actual consumed-build-run receipt and actual source/helper/manifest hashes, preserve scope/ceilings and no-deletion policy, and cite #592 for this readback. Do not submit any original old plan verbatim.
- Run current preflight, watched retention report and fresh admission through the existing tools. Submit the exact run.sh with the existing watch-build-submit owner and retain original command/monitor/runner/launcher/tool-wrapper/timeout outcomes. No watcher or receipt producer is changed here.
- After actual completion, require artifact result PASS, complete six selected rows, original channels0 and actual owner absence before root consumes the allocation. Keep original failures unchanged. Final installed agent must consume these actual inputs/result hashes; the source packet is not their replacement.

The existing generic commands remain tools/build-preflight; tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report with the materialized plan/report; tools/host-maintenance/build-admission prepare; tools/watch-build-submit with the new admission and run.sh; and build-admission consume with root-reviewed original consumption-evidence. No command in this paragraph ran during preparation.

## Old-cache consumer closure

old-cache-consumer-closure.json records this lane's completed source reads. The old cache path appears only as historical manifest provenance. The derivative uses source_relative under the NEW build-inputs root and never opens manifest source_path. All needed original verifier/small receipt bytes are copied here. This lane has no remaining old-cache reader and requires no retained old-cache alias. This is a lane-specific closure, not a host-wide quiescence assertion; root still owns the actual relocation census.

No engineering image has been built or read by this packet, no installed/resource/gameplay proof has run, and no RC/audit/deployment/publication clearance is implied.
