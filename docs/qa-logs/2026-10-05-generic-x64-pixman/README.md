# GENERIC_X64 software compositor fallback

Issue #447. Maintainer: "Let's proceed with this fix."

Can this be done on the VM? Yes. Real software and virgl guests verify
capability selection. Image-BusyBox chroot controls exercise missing,
malformed, non-virtio, explicit-override and multi-card boundaries. Those
synthetic controls prove selection only, with compositor exec replaced by a
recorder; they do not prove installed rendering.

The only shipped changes are a GENERIC_X64 Sway service drop-in and its
wrapper. Shared Sway, handheld packages, application drivers and saved
settings are unchanged. Valid negotiated virtio feature bit0 clear selects
Pixman; virgl or an explicit renderer/render-device selection remains intact.
Unknown devices or capability strings retain existing behavior.

Kernel source inspected in the exact frozen09 linux-7.1.2 build:
`drivers/virtio/virtio.c:features_show` emits negotiated bits lowest first;
`include/uapi/linux/virtio_gpu.h` defines VIRTIO_GPU_F_VIRGL as0;
`drivers/gpu/drm/virtio/virtgpu_drv.c` sets DRIVER_RENDER unconditionally
and registers DRM against the transport parent. The features belong to its
virtio child, selected beneath the chosen card only.
Thus render-node absence/presence would not identify the affected mode.
The earlier matched renderer evidence lives in replacement09's
`historical-render-comparison/pixman.md` and `signin-ui-13/`.

Already written: old /storage Sway configuration remains readable. No new
persistent setting or marker is introduced; selection occurs at every service
start using the card chosen by existing boot initialization. Installation on
an upgraded SYSTEM must be proved as well as a fresh boot.

Selector04 passes all22 selection checks on each actual software/virgl guest
(44 total), with the image BusyBox and retained real transport/virtio paths.
All four terminal channels are0. Actual415e17 cleanup19:06:35 verifies all
six owner/guest PIDs absent and no QEMU. Build-log SHA
`c3fefe4c244c9a355a97a1b498c79cb602c9612d9adcfbc4f70343b80a7f9a64`.

Selector01 failed on the direct-device sysfs assumption. Selector02 failed
before wrapper execution because its fixture used /lib instead of the image
/usr/lib loader layout (#450). Selector03 passed22 software cases but could
not authenticate after restart: read-only serial metadata shows active sshd
and an empty0600 QA key file. Fresh04 syncs writes before stopping and follows
existing per-boot key provisioning. All three original all-1 results remain
failed; their22 owner/guest PIDs including successful04 were checked absent.
The four retained directories carry114 hash-bound evidence members.

Current state: source selection proof passed; rebuilt image not yet qualified.
Next: integrate/freeze/build, then clean/upgrade software and accelerated
selection, exact sign-in pixels, ES/emulator launch/exit and time-to-play on
those bytes. #447 remains open. Runtime fixture proof does not qualify
packaging or compositor rendering. No personal device/cloud was touched.
