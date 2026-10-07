#!/bin/bash
set -euo pipefail
O=/tmp/pixelelated-508-es-host04
E=/home/max/Development/emulationstation-next.worktrees/m7-manual-cloud-setup
D=/workspace/repos/rocknix.worktrees/conflict-resolution
B=/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16/build.pixelelated-GENERIC_X64.x86_64
export TMPDIR="$O/tmp" CCACHE_DISABLE=1
trap 'rc=$?; printf "%s\n" "$rc" > "$O/inner.rc"' EXIT
mapfile -t CPP < <(git -C "$E" diff --name-only | sed -n '/^es-app\/src\/.*\.cpp$/p' | sed "s#^#$E/#")
"$D/tools/es-syntax-check" --root "$B" "${CPP[@]}" | tee "$O/artifacts/syntax.log"
"$D/tools/vocabulary-check" --es "$E" | tee "$O/artifacts/vocabulary.log"
"$B/toolchain/bin/msgfmt" --check --check-format -o "$O/artifacts/fr.mo" "$E/locale/lang/fr/LC_MESSAGES/emulationstation2.po" 2>&1 | tee "$O/artifacts/msgfmt.log"
"$B/toolchain/bin/xgettext" --add-comments=TRANSLATION --keyword=_ --no-location -o "$O/artifacts/changed.pot" "${CPP[@]}" 2>&1 | tee "$O/artifacts/xgettext.log"
git -C "$E" diff --check
python3 "$E/tests/cloud-oauth-lifetime.py" | tee "$O/artifacts/oauth-lifetime.log"
"$B/toolchain/bin/cmake" -S "$E/es-app/tests/unit" -B "$O/unit" -DCMAKE_CXX_COMPILER=/usr/bin/g++ -DRAPIDJSON_INCLUDE_DIR="$B/toolchain/x86_64-rocknix-linux-gnu/sysroot/usr/include" > "$O/artifacts/unit-configure.log" 2>&1
"$B/toolchain/bin/cmake" --build "$O/unit" --target es-unit-tests -j4 > "$O/artifacts/unit-build.log" 2>&1
"$O/unit/es-unit-tests" > "$O/artifacts/unit-result.log" 2>&1
python3 "$O/build.py"
