# Support matrix for pixelelated 0.0.1 (#344)

## Current accepted evidence and held assets — 2026-10-07

D-CLOUD-177/178 and #510 hold new device builds and product integration until
the agreed validator flow is reconciled and qualified. Public ROCKNIX and clean installs define cloud adoption;
the maintainer's experimental layouts remain historical receipts, not a
separate product requirement. Accepted artifacts below are unchanged.

The approved targets remain GENERIC_X64 for QA, H700 for the two named boards,
and SM8550 for Nova (D-WORKFLOW-114/124). RG35XX SP is the mandatory adoption
device. RK3566 remains deferred. M7's ordered body controls execution; each
asset needs its own recorded smoke evidence before attachment (D-WORKFLOW-120).

| Target / arch | Physical board | QA guest | Current clean-install evidence | Current upgrade evidence | Boot medium/chain and remaining disposition | Recovery method | Attachment status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GENERIC_X64 / x86_64 | none | candidate16 isolated guests | candidate16 `ee01490913`: 15 default suites and 78 screens accepted | 26 actual RC2 retained-storage upgrade checks accepted | canonical VM profile; candidate16 identity and raw/update evidence accepted; release input/asset mapping remains | recreate disposable guest from retained candidate and fixtures | held for remaining manifest/source/publication gates |
| H700 / aarch64 + arm | RG35XX SP, LPDDR4/DDR4; mandatory adoption device | none | no new candidate clean-card observation claimed; September baseline below remains historical | #500: ROCKNIX `69e6039f8f` to pixelelated `43d0bc3bf4`, authorized transfer/reboot and exact installed bytes accepted 2026-10-07 | microSD; exact SP DTB and DDR4 bootloader match accepted firmware; original mounts retained; clean-versus-upgrade/downgrade and broader smoke dispositions remain | recorded route: reflash microSD; recovery media/runbook below; no new recovery trial claimed | firmware/adoption accepted; broader smoke and release gates outstanding; held |
| H700 / aarch64 + arm | RG SP, LPDDR3/DDR3 | none | no pixelelated candidate clean-card observation | no pixelelated candidate adoption proof; older observations below are historical | DDR3 firmware artifact accepted; physical board selection, boot and smoke still require their named evidence | recorded route: reflash microSD; no new recovery trial claimed | artifact accepted; board adoption/smoke and release gates outstanding; held |
| SM8550 / aarch64 + arm | Retroid Pocket Nova | none | no pixelelated candidate clean-card observation | no pixelelated candidate adoption proof | microSD/GPT/ABL; build04 and independent acceptance04 passed at 16:52 UTC on0553; GPT/ABL and raw/update payload equality verified; physical ABL/boot-chain/smoke evidence remains separate | recorded route: reflash microSD; internal-storage recovery implications must be stated from the accepted boot-chain evidence | artifact accepted; named physical and release gates outstanding; held |
| RK3566 / aarch64 + arm | RG353M | none | outside this release | outside this release | deferred by D-WORKFLOW-114 | historical route below | not built or attached for 0.0.1 |

Primary records: [candidate16 qualification](../qa-logs/2026-10-07-pixelelated-replacement-16/README.md),
[H700/SP acceptance](../qa-logs/2026-10-07-device-builds/rg35xxsp-adoption01/README.md),
[SM8550 continuation04](../qa-logs/2026-10-07-device-builds/sm8550-resume04/README.md)
and [device facts](../releases/device-facts.md). H700 artifact acceptance covers
both DDR variants; one board's successful adoption does not qualify the other.

No historical "deltas: none" below is asserted for the new candidate. Re-derive
the release's per-SoC boot-chain delta/downgrade disposition from exact inputs.
Do not replay accepted SP transfer/reboot or common VM qualification merely to
refresh this table. Further physical actions need their own named authority.

#508/D-CLOUD-175 replaces the cloud migration flow with manual folder setup.
Its script/UI proof is in progress; none of the accepted artifacts above yet
includes that replacement. Map and qualify those new inputs before selecting
release assets. Owner Dropbox reconciliation is separate from board QA.

## Historical matrix — 2026-09-30, updated 2026-10-01

The original observations and source-line references below are preserved as a
dated baseline. Their "not built", "deltas: none" and attachment statements do
not override the current table. Original physical observations are not renamed
into current candidate proof.

Build targets, the physical boards behind each, and what has been observed on them, from `docs/releases/catalog.md`, `docs/releases/device-facts.md`, the device options and the runbook. The **mandatory migration device is the RG35XX SP** (D-WORKFLOW-100). No boot-chain path has changed since RC2 (`git log 69e6039f8f..next` over `projects/ROCKNIX/devices/{H700,RK3566,SM8550,GENERIC_X64}`, `projects/ROCKNIX/bootloader`, the ABL and u-boot packages, both kernel recipes, both busybox recipes, `scripts/image`, `scripts/mkimage`, `distributions/ROCKNIX` is empty at `51f78ac5b4`); the deltas column is re-derived from the manifest at P2/P2b, since a bump between now and the candidate's build would change it.

| Target / arch | Physical boards | QA guest | Clean install (last observed) | Upgrade (last observed) | Boot medium and boot chain; deltas since RC2 | Recovery method | Attachment status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GENERIC_X64` / `x86_64` | none (a VM target of the fork's own) | guests a to d (`tools/vm-pair`, `generic-x64-vm`; 4 qcow2, 9.3 GB) | every `tools/vm-qa` run boots the image fresh: run 73 on `69e6039f8f` (RC2), 13 of 15 suites, `x64-all-20260929-69e6039f8f/RECORD.txt` | `tools/vm-upgrade-rehearsal` from RC1's image: `qa-69e6039f8f-upgrade-from-8dd6765af0-20260929-2243` | qcow2 or USB image, GPT, syslinux/GRUB (`devices/GENERIC_X64/options:20,27`), `DISK_LABEL="ROCKNIX"` (`:70`); deltas: none | re-import the image; nothing to recover on a guest | not built; nothing attached |
| `H700` / `aarch64` (+ `arm` root for 32-bit) | **RG35XX SP** (LPDDR4, DDR4 image; **mandatory migration device**), RG SP (LPDDR3, DDR3 image) | none (no aarch64 guest) | RG SP: DDR3 card flashed and read back 2026-09-05 19:16 UTC (work log); RG35XX SP: fresh card with `/dtb.img` activated 2026-09-05/06 (runbook § 5) | in place through `/storage/.update`: RG35XX SP on RC1 `8dd6765af0` 2026-09-29 05:48 UTC and RC2 `69e6039f8f` 22:44 UTC; RG SP on RC1 16:11 UTC, RC2 staged 22:5x (device facts rows 14-15; catalog) | microSD, msdos table, u-boot + ATF (`devices/H700/options:21,34,37`), the model's `/dtb.img` activated once on a fresh card, one update tar for both boards with the DDR3/DDR4 bootloader chosen by the running board; deltas: none | the supplied stock card kept as recovery media; reflash from the PC (`docs/device-flashing-runbook.md`) | not built; nothing attached |
| `SM8550` / `aarch64` (+ `arm`) | Retroid Pocket Nova | none | never from a fresh card by this fork: the Nova ran stock ROCKNIX 20260901 (`1ebff24f36`) and took the fork's images in place | RC1 `5b5005879e` 2026-09-29 19:31 UTC (the first fork image on the board), RC2 `69e6039f8f` 22:31 UTC (device facts rows 16, 24) | microSD, GPT, `BOOTLOADER="qcom-abl"` (`devices/SM8550/options:21,34`); the per-update `update.sh:21` writes "ROCKNIX ABL on SD" and `updateabl` writes the ABL to the internal eMMC/UFS by hand (`updateabl:5,19`); the chain from the internal bootloader to the card is quoted, not verified on the board -- a P2b read; deltas: none | reflash the microSD; the internal storage is untouched by an update (the ABL slot only by `updateabl`, which no update runs) | not built; nothing attached |
| `RK3566` / `aarch64` (+ `arm`) **-- deferred, not built for 0.0.1 (D-WORKFLOW-114, 2026-10-01)** | Anbernic RG353M | none | none recorded on the RG353M by any RC cut (`device-facts.md` has no RK3566 row; RC1's image "NOT staged", catalog row 17) | none recorded | microSD, GPT, u-boot with `rkbin` (`devices/RK3566/options:21,34,37`), two images (`-Generic`, `-Specific`); deltas: none, but **no board observation since RC2 at all** | reflash from the PC | **held pending device verification** (base plan §2.1: built from the same manifest, listed in the notes, attached when its smoke test is recorded) |

The Nova's panel is 1280x960 and the H700 boards' 640x480, both 4:3 (read from the Nova 2026-10-01; the H700 is the fork's own frame size); the first 16:9 board is a device the maintainer has yet to buy (D-WORKFLOW-114).

Not in the matrix: `RK3326` (RG351M; dropped from the roster 2026-09-30, D-WORKFLOW-092), every other ROCKNIX target (they build from `upstream/next` merges and are neither built nor published by the fork).

Two facts the VM cannot supply and the matrix depends on (`vm-first.md`): the H700 boards' bootloader selection by RAM type, and the Nova's ABL chain; both are device-facts rows (14-16, 24) and are re-read on the candidate at P2b/P3 with the owner's yes for the copy and for the reboot (D-QA-011).
