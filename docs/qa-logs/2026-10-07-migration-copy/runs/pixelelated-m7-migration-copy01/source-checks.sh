#!/bin/bash
set -euo pipefail
TASK_OWNER=/tmp/pixelelated-m7-migration-copy01
ES_TREE=/home/max/Development/emulationstation-next.worktrees/m7-migration-copy
DISTRIBUTION=/workspace/repos/rocknix.worktrees/conflict-resolution
ES_BUILD_ROOT=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/build.pixelelated-GENERIC_X64.x86_64
export ES_BUILD_ROOT TMPDIR="$TASK_OWNER/tmp" CCACHE_DISABLE=1
trap 'rc=$?; printf "%s\n" "$rc" > "$TASK_OWNER/inner.rc"' EXIT
"$DISTRIBUTION/tools/es-syntax-check" "$ES_TREE/es-app/src/guis/GuiMenu.cpp" | tee "$TASK_OWNER/artifacts/syntax.log"
"$DISTRIBUTION/tools/vocabulary-check" --es "$ES_TREE" | tee "$TASK_OWNER/artifacts/vocabulary.log"
GETTEXT_BIN="$ES_BUILD_ROOT/toolchain/bin"
"$GETTEXT_BIN/msgfmt" --check --check-format -o "$TASK_OWNER/artifacts/fr.mo" "$ES_TREE/locale/lang/fr/LC_MESSAGES/emulationstation2.po" 2>&1 | tee "$TASK_OWNER/artifacts/msgfmt.log"
"$GETTEXT_BIN/xgettext" --add-comments=TRANSLATION --keyword=_ --no-location -o "$TASK_OWNER/artifacts/GuiMenu.pot" "$ES_TREE/es-app/src/guis/GuiMenu.cpp" 2>&1 | tee "$TASK_OWNER/artifacts/xgettext.log"
git -C "$ES_TREE" diff --check
printf '%s\n' 'PASS exact edited source syntax, vocabulary, French format, and xgettext extraction; rendered UI pending.'
