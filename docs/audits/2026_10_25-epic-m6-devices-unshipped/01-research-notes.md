# Research notes — M6.P2 T25, the devices the fork does not ship and the other projects (#672)

## Scope

- **The read hash:** `8ebaf8daad`. The 397 are byte-equal at the dispatch tip `b27889bce2` (c03 `[]`). **`reviewed-at`:** `b27889bce2`. **Upstream read:** `651150fc88`, by name; the inventory's own upstream read was the older `c1f1746828`. **Base:** `c445081a59` (the `20261001` tag).
- **The block** (brief § 2, `stage-a/scope.sh`, c01):

  ```text
  paths 397 lines 49555 {'unreached': 216, 'unshipped': 181} {'upstream-carried': 396, 'fork-own': 1}
  units 25
  read 3619 rows 64 fork-own 0
  shadowed 9 fork-own ['packages/linux/package.mk']
  ```

  The 397 are in `stage-a/paths.txt`, with each row's reach, tier, lines, language, `buildable_by` and `shadowed_by` in `stage-a/rows.tsv`. Languages: devicetree 53, shell 95, recipe 52, config 50, none 32, other 24, yaml 21, text 15, markdown 11, xml 11, udev 8, systemd 7, symlink 6, python 4, c 3, image 3, make 1, script 1.
- **The units (25), as the block prints them** (every count matches the brief's table):

| Unit | Paths | Lines | Reach |
| --- | ---: | ---: | --- |
| `projects/ROCKNIX/devices/AMD64` | 15 | 494 | unshipped 13, unreached 2 |
| `projects/ROCKNIX/devices/RK3326` | 37 | 9,880 | unshipped |
| `projects/ROCKNIX/devices/RK3399` | 4 | 1,554 | unshipped |
| `projects/ROCKNIX/devices/RK3566` | 16 | 3,953 | unshipped |
| `projects/ROCKNIX/devices/RK3576` | 6 | 1,907 | unshipped |
| `projects/ROCKNIX/devices/RK3588` | 3 | 212 | unshipped |
| `projects/ROCKNIX/devices/S922X` | 4 | 207 | unshipped |
| `projects/ROCKNIX/devices/SM4450` | 18 | 7,278 | unshipped |
| `projects/ROCKNIX/devices/SM6115` | 16 | 2,502 | unshipped |
| `projects/ROCKNIX/devices/SM8250` | 28 | 7,653 | unshipped |
| `projects/ROCKNIX/devices/SM8650` | 8 | 2,298 | unshipped |
| `projects/ROCKNIX/devices/SM8750` | 14 | 4,192 | unshipped |
| `projects/ROCKNIX/packages/{linux-drivers,linux-firmware}` | 15 | 1,264 | unshipped 14, unreached 1 |
| `projects/ARM` · `Allwinner` · `Amlogic` · `Generic` · `NXP` · `Qualcomm` · `RPi` · `Rockchip` · `Samsung` | 4 · 24 · 19 · 19 · 25 · 7 · 28 · 35 · 12 = 173 | 4,987 | unreached, all |
| `packages/linux` · `packages/linux-driver-addons` · `packages/linux-firmware` | 4 · 14 · 22 = 40 | 1,174 | unreached, all |

- **The provenance:**
  - against the base: **1 M**, `packages/linux/package.mk` (c07);
  - against `651150fc88`: **39 M** (c08), with **65** upstream commits since the base (c09);
  - every fork commit touching a target directory is one of the fork's merges of upstream (c10).
- **The weight:** **1,424,530 bytes** (c15).
- **The positive control:** the shipped pair's two target lines (c16); the block with reach `shipped` and `/H700/` returns 28 rows (c17).
- **Deltas from the brief:** none in the figures. RPi's whole-word engine count is 2, and `scripts/image:349` is a substring (`Distro_RPi`) in a comment (`00`).
