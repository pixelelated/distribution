# T37 (#684): the window's commands, sourced by each step (bash). Paths and sockets only. Only
# vm-serial's `sh` is used: its `script` uploads a file, and the guest writes nothing.
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684
A=$D/docs/audits/2026_11_01-epic-m6-es-recipe
GC=$A/guest-cycle
G=/workspace/tmp/m6-t37/guest
VM=$D/projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm
HELP=$GC/helpers
FILTER='key|pass|token|user|psk'
ser() { "$D/tools/vm-serial" --socket "$G/serial.sock" --timeout "${T:-60}" sh "$*"; }
census() { bash "$HELP/census.sh"; }
boot() { QEMU_SYSTEM_X86_64="$HELP/qemu-wrap" "$VM" run --headless --daemonize --res 640x480 --serial "$G/serial.sock" --pidfile "$G/qemu.pid" "$G/disk.qcow2"; }
waites() { "$D/tools/vm-serial" --socket "$G/serial.sock" --timeout 240 wait; }
