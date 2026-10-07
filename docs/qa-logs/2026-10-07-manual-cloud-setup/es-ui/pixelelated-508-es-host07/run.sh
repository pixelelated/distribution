#!/bin/bash
set -euo pipefail
O=/tmp/pixelelated-508-es-host07
E=/home/max/Development/emulationstation-next.worktrees/m7-manual-cloud-setup
D=/workspace/repos/rocknix.worktrees/conflict-resolution
B=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/build.pixelelated-GENERIC_X64.x86_64
export TMPDIR="$O/tmp" CCACHE_DISABLE=1
trap 'rc=$?; printf "%s\n" "$rc" > "$O/inner.rc"' EXIT
mapfile -t CPP < <(git -C "$E" diff --name-only | sed -n '/^es-app\/src\/.*\.cpp$/p' | sed "s#^#$E/#")
"$D/tools/es-syntax-check" --root "$B" "$E/es-app/src/guis/GuiMenu.cpp" | tee "$O/artifacts/syntax.log"
"$D/tools/vocabulary-check" --es "$E" | tee "$O/artifacts/vocabulary.log"
"$B/toolchain/bin/msgfmt" --check --check-format -o "$O/artifacts/fr.mo" "$E/locale/lang/fr/LC_MESSAGES/emulationstation2.po" 2>&1 | tee "$O/artifacts/msgfmt.log"
"$B/toolchain/bin/xgettext" --add-comments=TRANSLATION --keyword=_ --no-location -o "$O/artifacts/changed.pot" "${CPP[@]}" 2>&1 | tee "$O/artifacts/xgettext.log"
git -C "$E" diff --check
python3 "$O/build.py"
