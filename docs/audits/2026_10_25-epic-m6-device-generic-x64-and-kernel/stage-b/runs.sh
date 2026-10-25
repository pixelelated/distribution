#!/bin/bash
# T11 (#658) stage B: the brief's section 5 runs and stage B's reads, each
# with its exit and wall time. Read-only: no fetch, no build, no guest, no
# tools/council/run. Run from the lane's worktree; outputs under $OUT.
set -u
D=/workspace/repos/pixelelated/distribution.worktrees/m6-device-generic-x64-658
cd "$D" || exit 2
export TMPDIR=/workspace/tmp/m6-t11/tmp
OUT=/workspace/tmp/m6-t11/runner/out
mkdir -p "$TMPDIR" "$OUT" .qa-scratch/t11
R=8ebaf8daad
U=651150fc88
C=projects/ROCKNIX/devices/GENERIC_X64/linux/linux.x86_64.conf
M7=/workspace/repos/rocknix.worktrees/m7-signin-generic-build-20261025-01
M7B=$M7/build.pixelelated-GENERIC_X64.x86_64
printf 'id\trc\tseconds\tstarted_utc\n' > "$OUT/runs.tsv"

run() {
  local id=$1; shift
  local t0 t1 rc started
  started=$(date -u +%H:%M:%S)
  t0=$(date +%s.%N)
  ( "$@" ) > "$OUT/$id.out" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  printf '%s\t%s\t%.2f\t%s\n' "$id" "$rc" "$(echo "$t1 - $t0" | bc)" "$started" >> "$OUT/runs.tsv"
}

r01_scope() { bash /workspace/tmp/m6-t11/runner/scope.sh; }
r02_config_diffs() {
  for b in projects/Generic/linux/linux.x86_64.conf projects/ROCKNIX/devices/AMD64/linux/linux.x86_64.conf; do
    git show "$R:$b" > "$TMPDIR/base.conf" || return 1
    git show "$R:$C" > "$TMPDIR/ours.conf" || return 1
    echo "$b removed=$(diff "$TMPDIR/base.conf" "$TMPDIR/ours.conf" | grep -c '^<') added=$(diff "$TMPDIR/base.conf" "$TMPDIR/ours.conf" | grep -c '^>')"
  done
  echo "ours lines $(git show "$R:$C" | wc -l)"
}
r03_config_header() { git show "$R:$C" | sed -n '3p'; }
r04_recipe_version() { git show $R:projects/ROCKNIX/packages/linux/package.mk | sed -n '30,45p' | grep -n -E 'PKG_VERSION|GENERIC_X64'; }
r05_recipe_oldconfig() { git show $R:projects/ROCKNIX/packages/linux/package.mk | grep -n -E 'listnewconfig|oldconfig'; }
r06_conf_fork_edits() { git log --format='%h %ad %an %s' --date=short 73b20caf86..$R -- "$C"; }
r07_conf_fork_lines() { git log -p --format='=== %h' 73b20caf86..$R -- "$C" | grep -E '^[-+][^-+]'; }
r08_history() {
  tr '\n' '\0' < .qa-scratch/t11/paths.txt | xargs -0 git log --no-merges --format='%h %an' --since=2026-06-01 $R -- > "$TMPDIR/hist.txt" || return 1
  echo "total $(wc -l < "$TMPDIR/hist.txt")"
  echo "fork $(grep -c -E ' (Max Engel|blitterbot|rasterabot)$' "$TMPDIR/hist.txt")"
  echo "upstream $(grep -v -c -E ' (Max Engel|blitterbot|rasterabot)$' "$TMPDIR/hist.txt")"
}
r09_upstream_delta() { tr '\n' '\0' < .qa-scratch/t11/paths.txt | xargs -0 git diff --name-status $R $U -- | awk '{print $1}' | sort | uniq -c; }
r10_boot_runners() { git grep -n -E 'bootloader/(install|mkimage|release|rkhelper)' $R -- scripts config | cut -c1-140; }
r11_install_branches() { git show $R:projects/ROCKNIX/bootloader/install | grep -n -E '^\s*[a-z|"-]*\)|^\s*\*\)'; }
r12_install_upstream() { if git cat-file -e $U:projects/ROCKNIX/bootloader/install 2>/dev/null; then echo upstream-has-install; else echo fork-only-install; fi; }
r13_bootloader_per_device() { git grep -n -E '^\s*BOOTLOADER=' $R -- 'projects/ROCKNIX/devices/*/options' | cut -c1-110; }
r14_rkhelper_readers() { git grep -n rkhelper $R -- scripts projects packages tools | grep -v ':projects/ROCKNIX/bootloader/rkhelper:' | cut -c1-140; }
r15_generic_recipe_mark() { git log --format='%h %ad %an %s' --date=short $R -- packages/linux/package.mk | head -5; }
r16_override_fork_commits() { git log --no-merges --since=2026-06-01 --format='%h %ad %an %s' --date=short $R -- projects/ROCKNIX/packages/linux/package.mk | grep -E 'Max Engel|blitterbot|rasterabot'; }
r17_launcher_functions() { git show $R:projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm > "$TMPDIR/gxv.py" && python3 -I -B -c 'import ast,sys; t=ast.parse(open(sys.argv[1]).read()); print(len([n for n in ast.walk(t) if isinstance(n,ast.FunctionDef)]),"functions")' "$TMPDIR/gxv.py"; }
r18_launcher_callers() { git grep -n -E 'generic-x64-vm' $R -- tools .claude/rules/generic-x64-vm-testing.md | cut -c1-140; }
r19_launcher_flags() { git show $R:projects/ROCKNIX/devices/GENERIC_X64/vm/generic-x64-vm | grep -n -o -E '"--[a-z-]+"|add_parser\("[a-z-]+"' | sort -t: -k2 -u; }
r20_vmpair_call() { git show $R:tools/vm-pair | grep -n -E 'VM_TOOL' | cut -c1-240; }
r21_no_tools_generic() { if git cat-file -e $R:tools/generic-x64-vm 2>/dev/null; then echo tools-generic-x64-vm-exists; else echo no-tools-generic-x64-vm; fi; }
r22_removal_rule() { echo "dispatch tip: $(git diff --stat 2103f0271d HEAD -- packages projects tools | tail -1)"; echo "read hash packages+projects: $(git diff --stat $R HEAD -- packages projects | tail -1)"; }
r23_firmware_lists() { git ls-tree -r --name-only $R projects/ROCKNIX | grep -E 'kernel-firmware.*\.dat$'; echo "x86_64.dat: $(git show $R:projects/ROCKNIX/packages/linux-firmware/kernel-firmware/firmwares/x86_64.dat)"; }
r24_built_config() {
  local f=$M7B/build/linux-7.1.2/.config
  stat -c '%y %s' "$f" || return 1
  sed -n '3p' "$f"
  git -C "$M7" log -1 --format='m7 head %h %ad' --date=iso
  git -C "$M7" diff --quiet $R HEAD -- "$C" && echo "conf equal at m7 head" || echo "conf DIFFERS at m7 head"
  git show "$R:$C" > "$TMPDIR/ours.conf"
  echo "removed=$(diff "$TMPDIR/ours.conf" "$f" | grep -c '^<') added=$(diff "$TMPDIR/ours.conf" "$f" | grep -c '^>')"
  python3 -I -B /workspace/tmp/m6-t11/runner/cfgclass.py "$TMPDIR/ours.conf" "$f"
}
r25_installed_firmware() {
  local d
  d=$(ls -d "$M7B"/install_pkg/kernel-firmware-*/usr/lib/kernel-overlays/base/lib/firmware) || return 1
  echo "${d#"$M7B"/}"
  echo "bytes $(du -sb --apparent-size "$d" | cut -f1) files $(find "$d" -type f | wc -l)"
  ls -l "$M7"/target/*.tar | awk '{print $5, $NF}' | sed 's|.*/target/|target/|'
}
r26_bzimage() { stat -c '%s %y' "$M7B/build/linux-7.1.2/arch/x86/boot/bzImage"; echo "embedded firmware source bytes $(du -sb --apparent-size "$M7B/build/linux-7.1.2/external-firmware" | cut -f1) files $(find "$M7B/build/linux-7.1.2/external-firmware" \( -type f -o -type l \) | wc -l)"; }
r27_release_glob_sources() { git grep -n -E 'usr/share/bootloader' $R -- projects/ROCKNIX/packages/tools/rocknix-abl/package.mk projects/ROCKNIX/packages/rocknix/package.mk projects/ROCKNIX/devices/H700/packages/u-boot/package.mk projects/ROCKNIX/packages/linux/package.mk | cut -c1-140; }
r28_syslinux_readers() { git grep -n -E 'share/syslinux|share/bootloader' $R -- packages/tools/installer scripts/mkimage | cut -c1-140; git ls-tree -r --name-only $R projects/ROCKNIX/devices/GENERIC_X64 | grep -c bootloader/ ; }

for f in $(declare -F | awk '{print $3}' | grep -E '^r[0-9]{2}_' | sort); do run "$f" "$f"; done
cat "$OUT/runs.tsv"
