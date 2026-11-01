#!/bin/bash
# T37 (#684) stage C: the lane's own reads of the seat's narrowing claims and added findings (no
# second packet is sent). Read-only: git by hash, and the export for the sourced build order.
cd /workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684 || exit 2
G=/usr/bin/grep; P1=2174265e9c; Q=/home/max/Development/emulationstation-next.worktrees/qa-integration; PIN=16dbac5211eea7e70db7394372033be2be7df829
echo "== PL-04: the pin's Splash.h:1-25"; git -C "$Q" show "$PIN:es-core/src/Splash.h" | awk 'NR<=25 {printf "%d: %s\n", NR, $0}'
echo "== PL-09: 'log-path' anywhere in the pin's sources"; git -C "$Q" grep -n -c 'log-path' "$PIN" -- es-app es-core 2>&1 | head; echo "(no line above = no file names it)"
echo "== G-2: ARCH and TARGET_ARCH at recipe-load time"; $G -n -E '^\s*(export )?TARGET_ARCH=|TARGET_ARCH=' config/arch.x86_64 config/arch.aarch64 config/arch.arm 2>/dev/null | head -4; $G -n -E 'arch\.\$\{?ARCH|config/arch' config/options | head -3; $G -n -E 'TARGET_' tools/pkgcheck | head -3
echo "== G-3: armsx2-sa's devices and its Turnip"; f=$(git ls-tree -r --name-only $P1 -- projects packages | $G -E '/armsx2-sa/package.mk$'); echo "recipe: $f"; git show "$P1:$f" | $G -n -i -E 'turnip|case|SM[0-9]{4}|DEVICE' | head -15; git show "$P1:projects/ROCKNIX/packages/virtual/emulators/package.mk" | awk 'NR>=85 && NR<=92 {printf "virtual/emulators:%d: %s\n", NR, $0}'
echo "== G-4: the busybox override and the global"; git show "$P1:projects/ROCKNIX/packages/sysutils/busybox/package.mk" 2>&1 | $G -n -E '^\. |source |PKG_VERSION=|packages/sysutils/busybox' | head -5
echo "== G-5: get_env's selection"; git show "$P1:scripts/get_env" | awk 'NR>=8 && NR<=24 {printf "get_env:%d: %s\n", NR, $0}' | sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'
echo "== G-6: when compile commands print"; git show "$P1:config/functions" | awk 'NR>=372 && NR<=383 {printf "config/functions:%d: %s\n", NR, $0}'
echo "== G-7: the autostart step"; git show "$P1:projects/ROCKNIX/packages/ui/emulationstation/autostart/001-emulationstation" | awk 'NR>=8 {printf "001-emulationstation:%d: %s\n", NR, $0}'
echo "== G-8: the serial check's read"; git show "$P1:projects/ROCKNIX/packages/ui/emulationstation/sources/serial_number_check" | awk 'NR>=8 && NR<=24 {printf "serial_number_check:%d: %s\n", NR, $0}'
echo "== G-9: 02's L-20 row"; $G -n -E '^\| L-20 ' docs/audits/2026_11_01-epic-m6-es-recipe/02-forward-audit.md | cut -c1-400
echo "== G-1: the patch's two replacement lines (counts only)"; git show "$P1:projects/ROCKNIX/packages/ui/emulationstation/patches/x86_64/cpugov.patch" | $G -c -E '^\+.*get_available_cpu_governors'; git show "$P1:projects/ROCKNIX/packages/ui/emulationstation/patches/x86_64/cpugov.patch" | $G -c -E '^\+.*get_available_gpu_governors'
