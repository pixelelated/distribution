"""Write 02's coverage table: one row per path in rows.json, notes by rule."""
import json
import sys

rows = json.load(open(sys.argv[1]))
read = set(open(sys.argv[2]).read().split())

P = "projects/ROCKNIX/"
G = P + "devices/GENERIC_X64/"
NOTES = {
    P + "bootloader/install": ("`scripts/image:280` sources it for every device (`find_file_path`; no package carries its own, so nothing is shadowed). Branches: `syslinux` does work for GENERIC_X64; `u-boot` (H700) and `qcom-abl` (SM8550) echo by design (`:45-61`); `grub`, `systemd-boot`, `\"\"` and `*)` are reached by no device. Fork-only (`73b20caf86`, `7178f1b1f3`).", "F-03 (header), F-05 (unread copy), F-06 (unreached branches)", "tree"),
    P + "bootloader/mkimage": ("Sourced by `scripts/mkimage:225-263` for `u-boot`, `arm-efi` and `qcom-abl` when the device has no own `bootloader/mkimage`: H700 and SM8550 reach it; GENERIC_X64's syslinux path does not (`scripts/mkimage:142-180`). Upstream rewrote its SM branches at `651150fc88` (bls/dtb).", "carried; the upstream rewrite is T25's and T28's (F-09)", "tree"),
    P + "bootloader/release": ("`scripts/image:285`, every device: `cp -a ${INSTALL}/usr/share/bootloader/*` into `3rdparty/bootloader`. The glob has sources on all three shipped devices (H700 u-boot and dtbs; SM8550 `rocknix-abl` and the `rocknix` package; GENERIC_X64 `install`'s syslinux copy).", "carried; no finding", "tree"),
    P + "bootloader/rkhelper": ("Read by seven Rockchip u-boot recipes (RK3326 x2, RK3399, RK3566 x2, RK3576, RK3588) through `find_file_path bootloader/rkhelper`; no shipped device. The inventory's `shipped` is directory-level.", "F-08 (inventory reach); carried for ROCKNIX's Rockchip devices", "tree"),
    P + "config.xml": ("Read by the image step's `mkimage` for u-boot/abl devices: H700 (`:2`) and SM8550 (`:130`); GENERIC_X64 has no entry and its syslinux path reads none. Upstream changed the SM entries at `651150fc88`.", "carried; the upstream change is T28's (F-09)", "tree"),
    G + "filesystem/usr/lib/sway/sway-generic-x64": ("The compositor wrapper the drop-in below starts: Pixman only for a virtio GPU without virgl (`:26-35`), then `exec /usr/bin/sway.sh`. Fork-own, GENERIC_X64 only.", "positive (P17); no finding", "tree"),
    G + "filesystem/usr/lib/systemd/system/serial-debug-shell.service": ("The developers' root shell on ttyS0, gated `ConditionVirtualization=vm` and the console argument (`:18-20`); D-QA-053 keeps it and the unit says so (`:4-14`).", "positive; no finding", "tree"),
    G + "filesystem/usr/lib/systemd/system/sway.service.d/10-generic-x64-renderer.conf": ("Replaces sway's `ExecStart` with the wrapper above (`:2-3`).", "no finding", "tree"),
    G + "linux/linux.x86_64.conf": ("The guest's kernel configuration: header `Linux/x86 6.15.6` (`:3`); the recipe builds 7.1.2 and runs `oldconfig` over it (`package.mk:306`, `:315`). Nearest base the Generic conf (659 / 351). The fork's 13 lines survive the build; 18 values, 97 set and 137 new options differ in the built file.", "F-04 (provenance; the regeneration packet), F-02 (embedded firmware and the GPU drivers it carries)", "tool-run"),
    G + "options": ("Device knobs: `x86-64-v3` (`:15`), `BOOTLOADER=\"syslinux\"` (`:27`), virtio/vmware GL (`:36`), `SWAP_SUPPORT=\"no\"` (`:86`), serial console (`:76`), `INSTALLER_SUPPORT=\"yes\"` (`:91`). No line says why syslinux or where the kernel configuration came from.", "Q7 (F-10)", "tree"),
    G + "vm/README.md": ("The profile's guide for Linux/QEMU and macOS/UTM: the UTM bundle, networking, the loopback ssh cloud route (`:92-121`), a UTM bridged-mode workaround (`:123-138`).", "F-07 (the UTM text after D-QA-053)", "tree"),
    G + "vm/generic-x64-vm": ("The launcher (817 lines, 19 functions): `profile`, `qemu-args`, `run`, `utm` (`:785-795`). Run by `tools/vm-pair:74` through `VM_TOOL` (`:36`); no other tool runs it.", "§ The launcher; design sentence deferred", "tree"),
    G + "vm/profile.json": ("The canonical guest: q35, Haswell-v4, 4 CPUs, 8 GiB, UEFI, 16 GiB virtio-blk, virtio-gpu-gl, virtio-net with the fw_cfg ssh port, intel-hda. Read by the launcher (`:26`, `:47-48`).", "positive; no finding", "tree"),
    G + "vm/utm-bundle-readme.txt": ("Packed into the `utm` bundle; teaches the ssh + `rclone config` cloud route on a Mac.", "F-07", "tree"),
    P + "filesystem/etc/machine-info": ("`CHASSIS=handset` on every image (`98e1a30362`); WebKitGTK and hostnamed read it, the guest included so its frames are the handheld's (`:1-8`).", "positive; nine lines, no cost (Q5)", "tree"),
    P + "options": ("Project defaults (`SQUASHFS_COMPRESSION=\"zstd\"`, `SWAP_SUPPORT=\"yes\"`, ...); every device's options override.", "carried; no finding", "tree"),
    P + "packages/kernel-drivers/device-tree-overlays/package.mk": ("Compiles `${PKG_BUILD}/${DEVICE}/*.dts` and installs the `.dtbo`s and `dtb_overlay` (the selectors are `:13` and `:20`): on our devices only H700's source compiles.", "carried; no finding", "tree"),
    P + "packages/kernel-drivers/device-tree-overlays/sources/dtb_overlay": ("The overlay helper installed on every device but RK3326 that builds the package (H700 here).", "carried; no finding", "tree"),
    P + "packages/linux-drivers/rocknix-joypad/package.mk": ("The joypad module; H700 builds it, GENERIC_X64 sets `ROCKNIX_JOYPAD=\"no\"` (`options:79`). Upstream moved it to `hackbar/rocknix-joypad` `005033d1dd` at `651150fc88`.", "Q4: behind upstream; the next merge brings it (T25)", "tree"),
    P + "packages/linux-firmware/extra-firmware/package.mk": ("Copies `SM8550/*` for SM8550 (`:13-21`); nothing for H700 or GENERIC_X64. Upstream at `925dfb5efb`.", "Q4: behind upstream; the next merge brings it (T25)", "tree"),
    P + "packages/linux-firmware/kernel-firmware/firmwares/any.dat": ("Half of every device's fallback (`any.dat` plus `${TARGET_ARCH}.dat`, `kernel-firmware/package.mk`): H700 and SM8550 carry their own lists, so it reaches neither; on GENERIC_X64 it is read beside `x86_64.dat`'s `*`, which already takes everything.", "carried; no finding", "tree"),
    P + "packages/linux-firmware/kernel-firmware/firmwares/x86_64.dat": ("One line, `*`: the x86_64 fallback. GENERIC_X64 has no own list, so it installs all of linux-firmware: 6,158 files, 2,876,913,748 bytes in the M7 build root.", "F-01", "tool-run"),
    P + "packages/linux-firmware/kernel-firmware/package.mk": ("Copies linux-firmware 20260309 plus `extra-firmware/` into `.copied-firmware`, then installs what the device's list (or the arch fallback) names (`makeinstall_target`).", "F-01 (GENERIC_X64's fallback); F-17's stamp gap (T5 E6) bears on any new list", "tree"),
    P + "packages/linux/package.mk": ("The override kernel recipe: GENERIC_X64 7.1.2 (`:36-40`), the x86 firmware block (`:197-207`), `listnewconfig`/`oldconfig` (`:306-316`), the `.config` copied into `.image` (`:385`). Fork-own by `dc948f59aa` and `3d7c075f63`.", "F-02, F-04; Q4", "tree"),
    P + "packages/linux/sysctl.d/network.conf": ("`net.ipv4.tcp_no_metrics_save=1`, every device.", "carried; no finding", "tree"),
    P + "packages/linux/sysctl.d/qdisc.conf": ("`net.core.default_qdisc = fq_codel`, every device; upstream drops the line at `651150fc88`.", "carried; the upstream change is T25's", "tree"),
    P + "packages/linux/udev.d/10-bfq-sched.rules": ("bfq on `mmcbl*`; upstream narrows it to whole disks at `651150fc88`. The guest's virtio-blk is not `mmcbl*`.", "carried; the upstream change is T25's", "tree"),
    P + "packages/linux/udev.d/30-disable-wakeup.rules": ("Disables USB host controllers' wakeup (`ehci-pci|xhci_hcd`).", "carried; no finding", "tree"),
    P + "packages/linux/udev.d/40-usb_modeswitch.rules": ("Three modeswitch rules for USB Wi-Fi/NIC sticks.", "carried; no finding", "tree"),
}


def note(path):
    if path in NOTES:
        return NOTES[path]
    if "/device-tree-overlays/sources/H700/" in path:
        return ("H700's DDR3 overlay; the only source that compiles on a shipped device.", "carried; no finding", "tree")
    if "/device-tree-overlays/sources/" in path:
        return ("Compiled only when `DEVICE` names its directory; no shipped device does. The inventory lists it under H700 (package-level reach).", "F-08 (inventory reach); carried for ROCKNIX's devices", "tree")
    if "/extra-firmware/panels/" in path:
        return ("An H700 panel blob: named by H700's `config/kernel-firmware.dat` and built into its kernel; on GENERIC_X64 through `x86_64.dat`'s `*`.", "carried; the guest copy is F-01's", "tree")
    if "/extra-firmware/rtl_bt/" in path or "/extra-firmware/cirrus/" in path:
        return ("Named by no shipped device's list; installed only on GENERIC_X64 through `*`, where nothing loads it (the guest has no such device).", "carried for ROCKNIX's devices; the guest copy is F-01's", "tree")
    raise SystemExit("no note for " + path)


print("| Path | Tier | Reach | Read | What it is, and who reads it | Finding or disposition | proved |")
print("| --- | --- | --- | --- | --- | --- | --- |")
for r in rows:
    what, disp, proved = note(r["path"])
    lines = r["lines"] if r["lines"] is not None else "binary"
    print("| `%s` | %s | %s | %s | %s | %s | %s |" % (
        r["path"], r["tier"], r["reach"], "read (%s)" % lines if r["path"] in read else lines, what, disp, proved))
