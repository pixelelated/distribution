# T35 (#682): the window's commands, sourced by each step (bash). Paths and sockets only;
# every frame is read back after it is taken. Nothing here starts without the slot.
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-core-window-input-682
A=$D/docs/audits/2026_10_31-epic-m6-es-core-window-input
GC=$A/guest-cycle
HELP=$GC/helpers
G=/workspace/tmp/m6-t35/guest
VM=$D/projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm
HOSTFILE=/workspace/tmp/m7-m6-host-coordination.txt
ser() { "$D/tools/vm-serial" --socket "$G/serial.sock" --timeout "${T:-60}" sh "$*"; }
serscript() { "$D/tools/vm-serial" --socket "$G/serial.sock" --timeout "${T:-90}" script "$1"; }
shot() { "$D/tools/vm-visual-qa" --monitor "$G/monitor.sock" shot "$GC/$1.png" && echo "shot $1"; }
key() { "$D/tools/vm-visual-qa" --monitor "$G/monitor.sock" key "$@"; }
settle() { "$D/tools/vm-visual-qa" --monitor "$G/monitor.sock" settle; }
census() { bash "$HELP/census.sh"; }
boot() { # <WxH>
  QEMU_SYSTEM_X86_64="$HELP/qemu-wrap" "$VM" run --headless --daemonize --res "$1" \
    --monitor "$G/monitor.sock" --serial "$G/serial.sock" --pidfile "$G/qemu.pid" "$G/disk.qcow2"
}
waites() { "$D/tools/vm-serial" --socket "$G/serial.sock" --timeout 240 wait; }
frames() { # <prefix> <count> <gap s>: a sampler, in the background, for G-02/G-03
  local p=$1 n=$2 g=$3 i
  for i in $(seq -w 1 "$n"); do "$D/tools/vm-visual-qa" --monitor "$G/monitor.sock" shot "$GC/$p-$i.png" >/dev/null 2>&1; sleep "$g"; done
}
