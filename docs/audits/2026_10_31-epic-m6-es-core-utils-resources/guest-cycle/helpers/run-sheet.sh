# T36 (#683): the window's commands, sourced by each step (bash). Paths and sockets only.
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-core-utils-resources-683
A=$D/docs/audits/2026_10_31-epic-m6-es-core-utils-resources
GC=$A/guest-cycle
G=/workspace/tmp/m6-t36/guest
VM=$D/projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm
HELP=$GC/helpers
ser() { "$D/tools/vm-serial" --socket "$G/serial.sock" --timeout "${T:-60}" sh "$*"; }
serscript() { "$D/tools/vm-serial" --socket "$G/serial.sock" --timeout "${T:-90}" script "$1"; }
shot() { "$D/tools/vm-visual-qa" --monitor "$G/monitor.sock" shot "$GC/$1.png" && echo "shot $1"; }
key() { "$D/tools/vm-visual-qa" --monitor "$G/monitor.sock" key "$@"; }
settle() { "$D/tools/vm-visual-qa" --monitor "$G/monitor.sock" settle; }
census() { bash "$HELP/census.sh"; }
boot() { QEMU_SYSTEM_X86_64="$HELP/qemu-wrap" "$VM" run --headless --daemonize --res "$1" --monitor "$G/monitor.sock" --serial "$G/serial.sock" --pidfile "$G/qemu.pid" "$G/disk.qcow2"; }
waites() { "$D/tools/vm-serial" --socket "$G/serial.sock" --timeout 240 wait; }
