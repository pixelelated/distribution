# Native gameplay 03: qualified ordinary saves, partial native states

**READY: compact durable originals, statically verified.** Root accepted only
ordinary Wii entered-cell and Dreamcast high-score persistence through normal
ES-owned launches and cold relaunch. This is not full native-state qualification,
a release-candidate claim, or an inference that all M7 criteria are complete.

The original run is `20261015T014406Z-0a49998d` in frozen branch
`build/m7-p5-20261015-01`, source `d4af5a255f4778a6ecf63ca5b37e05a0f1c83e3a`,
ES `3178b832b8d134198b2b4eede4f725d4ed283f8c`. Native owner:
`/workspace/tmp/pix-m7-native-gameplay-20261015-03`.
Image SHA256: `84b1552e4d0ed67d97b603230d1acb0b22a852217054854a9c3fe42731772ff2`.
SYSTEM SHA256: `02bd89c50a34190bee14d33fad6587b737598454c0d9e182d240c4f0acade2a4`.

## Exact accepted scope

- Wii SuDokuL: input entered 4 into previously empty row 1, column 2; explicit
  ordinary Save and Quit, orderly Dolphin exit, cold ES launch and Continue
  visibly restored the same puzzle/cell. Both stopped SD copies contain the
  identical 415-byte ordinary save, SHA256
  `93c59b358920c1d4c4ccabdc54b4b745c89347adb55b6f8d762d4e9c7ea340ce`.
  Its saved grid differs from the original grid only at that cell. This is an
  entered value, not a solved-puzzle claim; the solution value there is 6.
- Dreamcast Tetris 2: a normally earned score of 164, game-over/high-score entry,
  explicit VMU save and cold ES relaunch visibly restored Player 1's score.
  Actual A1 VMU SHA256 is
  `5f72f36f9a91a381064a078516b2b8d87eafb6804e09306e537f0679c0fe0040`.
  Its `tetris2.sys` FAT chain and package CRC validate; the decoded tenth entry is
  Player 1 / 2026-10-14 / 164. Flycast native automatic states remained off.

The exact coordinator review and acceptance are retained as originals.
Admission `ebed7b8ebcc040f2ae09acdf7531f8ab` was consumed qualified at
2026-10-15T02:27:50.506234+00:00. The consumed receipt's evidence hash matches
acceptance.json; every acceptance evidence hash was independently checked.
The run's command/runner/monitor and controller/supervisor receipts are preserved.
Native engine wait status remains unknown under the existing ES-owned lifecycle;
normal return and process absence do not replace an engine wait status.

## Original export failure remains a failure

Original export: `/workspace/tmp/pix-m7-native-gameplay-evidence-20261015-03`.
Raw export watch run `20261015T021345Z-9aac0821` has command 1 / runner 1 /
monitor 0. `close.py:35` stopped at its 4,096-file ceiling after debugfs exited 0.
The original empty export-manifest and false verification flags are retained.

The actual guest manifest lists 10,954 unique payload files / 308,518,337 bytes.
With the manifest itself there are 10,955 files / 310,803,035 bytes, no symlinks.
Four packaged GameSettings copies contribute 7,480 files / 4,586,052 bytes.
Both the guest 448 MiB payload and export 513 MiB byte limits pass. Independent
supplemental and coordinator reads rehashed every original payload and matched
all path/size/SHA256 rows exactly. The supplemental result establishes byte
custody without rewriting the original export failure.

## What is retained

| Artifact | Contents |
| --- | --- |
| original-records.tar.gz + original-records.json | Exact existing 846-member archive: complete owner source, host actions, original lifecycle/watch receipts, all 66 PNG frames and their original review records. |
| failed-export-originals.tar.gz + member manifest | All original export top-level receipts/debugfs output, plus the raw failed export watch run. |
| guest-export-manifest.json.gz | Lossless gzip of the complete original guest manifest; uncompressed SHA256 `6e3e308f6dccb4d9aa58a69182d4f6893e2cfc50a551611aa4b340e0c8d1db94`. |
| selected-guest-originals.tar.gz + member manifest | 304 original files: every nonsnapshot guest receipt/action/process observation, snapshot inventories, selected actual input/config readbacks and logs, and actual VMU files. No SD disk or copied GameSettings payloads. |
| supplemental-readback.tar.gz + member manifest | All 45 exact files from supplemental seal `b5058c830def636dad41690807e81a9fdf1e9240f8f89f227798473800854fd6`: executed data-only sources/receipts, both ordinary Wii save files, extracted tetris2.sys and decoded bytes, source bindings and interpretation limits. |
| reviewed-frame-index.json | All 66 original coordinator review rows verbatim, with archive member and independently checked SHA256; includes failed/intermediate observations and corrections. |
| large-artifact-locators.json | Exact image/SYSTEM/game input and large SD/native-state identities and original locators. These original files were not deleted. |

Archive member manifests retain source paths, lengths and hashes. No image,
cache, input CDI, 128 MiB SD image or native state payload is duplicated here.
The compact archive is deliberately selected evidence; it is not a replacement
for the original full guest export. Static verification checks each retained
member, the lossless manifest, acceptance/consumption binding and frame hashes.

## Remaining native-state scope

Wii created `ID-SuDokuL-Wii.s01` (6,380,469 bytes, SHA256
`b94681ea311a1f9162136f1ae6883517f9f0c0e4bb99234ed3b39bf40ef377b5`).
The save notification and a subsequent paused scene are visible. The attempted
restore frame still says Decompressing State; completed manual restoration is
unproved by that frame. No full native manual restore claim is accepted.

Flycast native Slot 1 remained empty; no native state is in its retained
inventory. Manual Save/change/Load, enabled native automatic save/restore, and
the ES-global-auto off/on comparison remain unproved in this run. Existing
ordinary-save evidence stays accepted independently. The attached continuation
is an unrun proposal only; it does not edit the fixture or allocate another VM.

No original bytes, shared record, issue, source, admission, or runtime were
modified while creating this durable packet. Root owns integration and retention.
