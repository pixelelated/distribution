# T22 stage E: the streams' cases, kept on the branch (#669)

These are the cases from `docs/reviews/briefs/t22-streams.md` (`a6e7a12ad6`). Each fails on the file at the stage-D tip `0f7ece71e8` and passes on the fixed file. S2 and S4 were struck at the second window's RETURN.

- **The drivers** take the file first and `unfixed|fixed` second. They write only under `$TMPDIR`, print one verdict line last (`<s>: unfixed-expectation-met | fixed-expectation-met | UNEXPECTED ...`), and exit 0 when that expectation is met.
- **S1 runs under the initramfs busybox**, because `/init` runs under busybox ash with busybox's applets, and the host's tools differ: the host's `md5sum` (uutils) rejects busybox's `-s`, and this busybox's ash has no `command` builtin. `T22_BUSYBOX` names a copy of the image's initramfs busybox. This audit's copy came from an M7 build root and was copied into scratch; nothing runs there. Its source and identity:
  - `.../build.pixelelated-GENERIC_X64.x86_64/build/busybox-1.36.1/.x86_64-rocknix-linux-gnu-init/busybox`
  - sha256 `4ce43643f300b585233e4723aaa3380d79d3b2bbe7a4ffaa540888041dbc13a6`, `BusyBox v1.36.1 (2026-10-05 03:37:08 UTC)`
- **Run all of them:** `T22_BUSYBOX=<busybox> TMPDIR=<scratch> stage-e/run-all.sh <stage-D tree> <fixed tree>`.

| Stream | Bug | Driver | Unfixed (stage-D tip): the line it prints | Fixed: the line it prints |
| --- | --- | --- | --- | --- |
| S1 | #1105 (PL-02), #1106 (PL-03) | `s1/drive.sh`: `scripts/init`'s functions with the paths moved into scratch and the host-touching commands stubbed; `check_update` over a staged `.tar`, ten cases (a the kernel write fails, b the SYSTEM write fails, c success, e the kernel write fails with no room for a second copy; and the six rejections that go on to a normal start: d a wrong md5, f updating disabled, g the installed kernel missing, h no SYSTEM in the update, i an incompatible update, j no room) | `s1: unfixed-expectation-met (a failed write still says Update complete and leaves a torn file; each of the six rejections unmounts /storage and deletes the update)` | `s1: fixed-expectation-met (a failed write is named and leaves the previous pair; success unchanged; each of the six rejections keeps /storage and the update as .rejected)` |
| S3 | #1107 (PL-28) | `s3/drive.sh`: the quirk's port block over six fw_cfg values, then two boots of the whole quirk (boot 1 at the stage-D tip writes its command from `12x34`, boot 2 with the file under test). `T22_UNFIXED` names the stage-D file | `s3: unfixed-expectation-met (12x34 kept as 1234; the wrong command stays)` | `s3: fixed-expectation-met (1234 accepted; 12x34, 70000, 0 and empty refused; the earlier wrong command removed)` |

A crossed run (the fixed file as `unfixed`, the stage-D file as `fixed`) prints `UNEXPECTED` and exits 1, for each stream.
