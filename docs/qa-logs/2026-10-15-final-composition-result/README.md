# Final d4af composition: consumed retained update and fresh install

Both scoped VM runs passed and were reviewed and consumed by the coordinator. This packet preserves their original compact exports, readable key receipts, coordinator reviews and consumption records. Packaging performed only read-only artifact verification and writes to this new evidence directory; it ran no test, VM, preparer, admission, cleanup, staging or commit.

| Run | Original result and scope | Consumption |
| --- | --- | --- |
| Retained | Ordinary d6a→d4af update; selected synthetic state preserved; installed default loader PASS. VM lifecycle 163.096 seconds. | `5d262d1fefc9492c9f538c8d35dc1bb8`, 2026-10-15T01:37:10.223897Z |
| Fresh | Untouched first-boot policy PASS before provisioning; installed default loader PASS. VM lifecycle 46.606 seconds. | `63d3378b185648629bd69f12237b3983`, 2026-10-15T01:39:22.141117Z |

Both bind source `d4af5a255f4778a6ecf63ca5b37e05a0f1c83e3a`, ES `3178b832b8d134198b2b4eede4f725d4ed283f8c`, build `0.0.1-dev+20261015T011500Z.gd4af5a255f47`. The actual final image SHA256 is `84b1552e4d0ed67d97b603230d1acb0b22a852217054854a9c3fe42731772ff2`; the update tar SHA256 is `b1457d7db7d7c93551ec56e2b2b913b78399eaa6c9b831761a514d87ec3f8666`. The exact final readback inputs and result are preserved within each archive's original provenance/record tree.

Can this be done on the VM? Yes. First-boot selected-state policy, ordinary image update and installed dependency loading require no physical-device fact. These original runs used one 8 GiB, four-CPU guest with no NIC each; the actual QEMU argv and guest `lo`-only interface readback are retained. Retained used VNC 136; fresh used VNC 138.

## Retained evidence

[retained/artifact-review.json](retained/artifact-review.json) links the original owner/export/run and records verification of its original bytes. [state-before.json](retained/records/state-before.json) and [state-after.json](retained/records/state-after.json) record different boot IDs, all selected-state checks true, zero changed selected paths, preserved original receipts and removal of the private snapshot. The ordinary update consumed the actual new tar through the original stage/reboot lifecycle. There was no reseeding or repeat default backup.

The protected base carried accepted 20→d6a state; the preceding fac608 proof used an overlay. This result proves d6a→d4af, not fac608→d4af. Original [base-before.json](retained/records/base-before.json) and [base-after.json](retained/records/base-after.json) are identical: 8,631,549,952-byte base, SHA256 `cfa55b79c36dd6b7fa1186c2e32cacc8b5e253f749f64effb4ec61ff273e488d`, identical device/inode/mode/mtime. The base and prior evidence remain separately owned. The retained work budget was 4200 seconds plus 180 seconds cleanup.

## Fresh evidence

[fresh/artifact-review.json](fresh/artifact-review.json) and the original [clean/report.json](fresh/clean/report.json) show `pixelelated-selected-state-v1`, mode `first-boot`, status `pass`, blocked 0, errors 0 and boot readiness `clear`. The unchanged clean helper ran before guest loader provisioning; its original transport exit was 0 without timeout. [boot.json](fresh/records/boot.json) preserves the actual new BUILD_ID and current boot ID. No selected synthetic retained state, SSH configuration or guest helper media preceded the clean gate. Fresh work budget was 1800 seconds plus 90 seconds cleanup.

The original policy report carries its scope and limitations. It is a selected-state check, not a whole-image or arbitrary-secret scan, and it does not infer the provenance of all possible device data.

## Installed loader and custody

Each original `records/guest-command-{0,1,2}.json` preserves argv, stdout, stderr, timeout and original return code for `ldd /usr/bin/cloud-signin-window`, `ldd /usr/lib/gstreamer-1.0/gst-plugin-scanner` and `/usr/bin/gst-inspect-1.0 opengl`. All six original statuses are 0, with no timeout and empty stderr. Child ceilings remain 15/15/30 seconds; loader serial/host envelopes remain 130/150 seconds.

Each `records/guest-loader.json` records RTLD_NOW PASS, thirteen installed member hash/mode/resolved-path checks equal before/after and equal to the bound final artifact, a fresh default registry, unchanged selected bytes/modes, removed private runtime, and no remaining loader process. The actual 580,445-byte registry is retained inside each archive (SHA256 `3909dfcddf443ce49cfd94fd37c9402f1ba90222652f59f07c79bdf407a9cd34`). This establishes the installed executable/default registry and dependency closure; it does not claim a separate scanner child-exec trace.

All original launcher, tool-wrapper, build, command, monitor, runner and VM channels are 0. VM results record no cleanup error, forced host cleanup, remaining host child, surviving host process or live QEMU. The original exporter recorded owners gone; this packaging task did not perform a new host process census. Both `admission-consumed.json` files match the exact consumption-draft hash and retain the original result channels. Scratch remains held; this packet grants no deletion or retirement exception.

## Original integrity and limits

`retained/original-records.tar.gz` is unchanged from the original exporter: 139 files, 2,032,423 uncompressed bytes, SHA256 `257c1674eae6db2a11a94f292aca911da9bda12adf6d85c1b3eaa1d884b9567d`. `fresh/original-records.tar.gz` likewise preserves 85 files, 1,784,352 uncompressed bytes, SHA256 `e0043c4f0b1bdc7bbe897aeaffc2c44c650db9cce92db625b2570c98fdb9b17e`. Every archive member's length and SHA256 was independently compared with its original `original-records.json`; every readable receipt is byte-identical to its source and archived member. No archive is unpacked over a runtime owner. There are no VM disks, firmware-variable media, host temporary media or private selected configuration snapshots in these exports. Harness `config.json` files contain source/runtime bindings; they are not player configuration exports.

`ORIGINALS.json` maps every copied receipt to its original absolute path and records bytes/SHA256. `SHA256SUMS` covers all packet files except itself. Generated `artifact-review.json`, `packet-review.json` and this README are review annotations, not replacements for original status records. Historical `config.json` status `PREPARED_UNRUN` and exporter `acceptance_claimed:false` remain unchanged; the later coordinator review and consumed receipt establish their subsequent disposition.

The [source plan](../2026-10-15-final-composition-plan/README.md) remains read-only and unchanged, seal SHA256 `4c6aba98468a13820f98cc8e47efa88fa20cd9842ce9369cc6dc3d7665a91215`. This task checked every file named by that seal. Native gameplay, installed Dolphin startup/Sys, earlier UI/protocol proofs, audit, publication and hardware acceptance remain their own evidence scopes. No original failed attempt is changed, and no synthetic VM result is promoted to a real-account/provider, physical-device, native gameplay or abrupt-power claim.
