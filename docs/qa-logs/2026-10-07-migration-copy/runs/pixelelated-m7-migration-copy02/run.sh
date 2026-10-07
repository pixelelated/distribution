#!/bin/bash
set -euo pipefail
O=/tmp/pixelelated-m7-migration-copy02
ES=/home/max/Development/emulationstation-next.worktrees/m7-migration-copy
D=/workspace/repos/rocknix.worktrees/conflict-resolution
B=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/build.pixelelated-GENERIC_X64.x86_64
export TMPDIR="$O/tmp" CCACHE_DISABLE=1
trap 'rc=$?; printf "%s\n" "$rc" > "$O/inner.rc"' EXIT
"$D/tools/es-syntax-check" --root "$B" "$ES/es-app/src/guis/GuiMenu.cpp" | tee "$O/artifacts/syntax.log"
"$D/tools/vocabulary-check" --es "$ES" | tee "$O/artifacts/vocabulary.log"
"$B/toolchain/bin/msgfmt" --check --check-format -o "$O/artifacts/fr.mo" "$ES/locale/lang/fr/LC_MESSAGES/emulationstation2.po" 2>&1 | tee "$O/artifacts/msgfmt.log"
"$B/toolchain/bin/xgettext" --add-comments=TRANSLATION --keyword=_ --no-location -o "$O/artifacts/GuiMenu.pot" "$ES/es-app/src/guis/GuiMenu.cpp" 2>&1 | tee "$O/artifacts/xgettext.log"
git -C "$ES" diff --check
python3 "$O/build.py"
