#!/bin/bash
# T29 (#676) stage C: the seat's claims, re-read at their lines. Read-only.
set -u
D=/workspace/repos/pixelelated/distribution.worktrees/m6-os-device-quirks-676
cd "$D" || exit 2
export TMPDIR=/workspace/tmp/m6-t29/tmp
OUT=/workspace/tmp/m6-t29/runner-c/out
A=docs/audits/2026_10_25-epic-m6-os-device-quirks
Q=projects/ROCKNIX/packages/hardware/quirks/devices
mkdir -p "$TMPDIR" "$OUT"
printf 'id\trc\tseconds\tstarted_utc\n' > "$OUT/runs.tsv"
run() {
  local id=$1; shift
  local t0 t1 rc started
  started=$(date -u +%H:%M:%S); t0=$(date +%s.%N)
  ( "$@" ) > "$OUT/$id.out" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  printf '%s\t%s\t%.2f\t%s\n' "$id" "$rc" "$(echo "$t1 - $t0" | bc)" "$started" >> "$OUT/runs.tsv"
}
s() { git show "8ebaf8daad:$1"; }
c01_g2_callers() { git grep -n -E 'analog_sticks_ledcontrol "|ledcontrol "\$|ledcontrol \$\{|analog_sticks_ledcontrol \$' 8ebaf8daad -- projects/ROCKNIX/packages | cut -d: -f2- | sed 's|projects/ROCKNIX/packages/||' | head -20; s projects/ROCKNIX/packages/sysutils/system-utils/sources/scripts/ledcontrol | sed -n 14,17p; }
c02_g6_g7_start_and_seed() { s projects/ROCKNIX/packages/hardware/quirks/platforms/SM8550/030-led-control | grep -n 'DEVICE_BATTERY_LED_STATUS'; s projects/ROCKNIX/packages/sysutils/system-utils/sources/autostart/common/098-deviceutils | sed -n 31,37p; echo "enable_service in system-utils: $(s projects/ROCKNIX/packages/sysutils/system-utils/package.mk | grep -c enable_service)"; echo "led.* in the seed system.cfg: $(s projects/ROCKNIX/packages/rocknix/config/system/configs/system.cfg | grep -c -E '^led\.')"; }
c03_g9_g15_fixture() { python3 -I -B "$A/tools/t29-battery-unset.py" --expect unfixed; echo "--- the unfixed Nova file against the fixed expectation:"; python3 -I -B "$A/tools/t29-battery-unset.py" --expect fixed | tail -1; s "$Q/Retroid Pocket 6/bin/battery_led_status" > "$TMPDIR/rp6-battery"; echo "--- RP6, --redirect-paths:"; python3 -I -B "$A/tools/t29-battery-unset.py" --file "$TMPDIR/rp6-battery" --redirect-paths --expect unfixed | tail -1; echo "--- RP6 as the packet showed it (no redirect):"; python3 -I -B "$A/tools/t29-battery-unset.py" --file "$TMPDIR/rp6-battery" | tail -1; }
c04_g10_vm_flags() { s "$Q/QEMU Standard PC (Q35 + ICH9, 2009)/001-device_config" | grep -c -E '^DEVICE_[A-Z_]+='; }
c05_g11_g12_091() { s "$Q/QEMU Standard PC (Q35 + ICH9, 2009)/091-retired-vm-fixes" | sed -n '61,72p;91,96p'; d=$(mktemp -d "$TMPDIR/dl.XXXXXX"); ln -s "$d/nowhere" "$d/link"; [ -e "$d/link" ] && echo "dangling: -e true" || echo "dangling: -e false"; rm -f "$d/link"; rmdir "$d"; }
c06_g13_nova_led_test() { s tools/nova-led-test | sed -n 24,27p; s tools/nova-led-test | sed -n 54,55p; }
c07_g14_g20() { s "$Q/Retroid Pocket Nova/bin/ledcontrol" | sed -n 47,66p; s projects/ROCKNIX/packages/emulators/libretro/retroarch/scripts/call_achievements_hooks.sh | sed -n 8,17p; }
c08_g38_reach() { python3 -I -B - <<'PY'
import subprocess, os
H="8ebaf8daad"; Q="projects/ROCKNIX/packages/hardware/quirks/devices"
def git(*a): return subprocess.run(["git",*a],capture_output=True,text=True)
top=[e.split("\t",1)[1].rsplit("/",1)[1] for e in git("ls-tree","-z",H,"--",Q+"/").stdout.split("\0") if e]
def resolve(path, depth=0):
    r=git("ls-tree",H,"--",path).stdout.strip()
    if not r or depth>5: return None
    mode,typ,oid=r.split("\t")[0].split()
    if mode=="120000":
        return resolve(os.path.normpath(os.path.join(os.path.dirname(path),git("cat-file","-p",oid).stdout.strip())), depth+1)
    return oid if mode!="040000" else None
def entry_dir(name):
    r=git("ls-tree",H,"--",f"{Q}/{name}").stdout.strip()
    return entry_dir(git("cat-file","-p",r.split()[2]).stdout.strip()) if r.split()[0]=="120000" else name
unq='[ ! ${BAT_LED_STATE} == "battery" ]'
hits=[(n,entry_dir(n)) for n in top if (o:=resolve(f"{Q}/{entry_dir(n)}/bin/battery_led_status")) and unq in git("cat-file","-p",o).stdout]
print(len(hits),"model names reach the unquoted test:", "; ".join(n if n==d else f"{n} (alias of {d})" for n,d in sorted(hits)))
PY
}
c09_g25_headers() { s "$Q/AYN Odin 2/bin/analog_sticks_ledcontrol" | sed -n 5,8p; s "$Q/Anbernic RG40XX V/bin/analog_sticks_ledcontrol" | sed -n 5,8p; }
for f in $(declare -F | awk '{print $3}' | grep -E '^c[0-9]{2}_' | sort); do run "$f" "$f"; done
cat "$OUT/runs.tsv"
