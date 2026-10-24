#!/bin/bash
# es-menu-map-check.sh -- tools/es-menu-map-check's control (T10 S9, #951):
# the tool, copied into a throwaway root under .qa-scratch/ beside a
# constructed map, over a constructed EmulationStation repository with one
# literal-titled page and one computed-titled page. Never the real checkout.
#   es-menu-map-check.sh [es-menu-map-check] [scratch-parent]
set -u
HERE="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
ROOT="$(cd "${HERE}/../../.." && pwd)"
TOOL="$(readlink -f "${1:-${ROOT}/tools/es-menu-map-check}")"
PARENT="${2:-${ROOT}/.qa-scratch}"; mkdir -p "${PARENT}" || exit 2
S="$(mktemp -d -p "$(cd "${PARENT}" && pwd)" es-menu-map.XXXXXX)" || exit 2
trap 'rm -rf "${S}"' EXIT
fail=0
check() { if eval "$2"; then echo "  ok    $1"; else echo "  FAIL  $1"; sed 's/^/          /' "${S}/out" | tail -4; fail=1; fi; }
mkdir -p "${S}/r/tools" "${S}/r/docs"; cp "${TOOL}" "${S}/r/tools/es-menu-map-check"
printf '# Menu map\n\n## SYSTEM SETTINGS\n\nThe page.\n' > "${S}/r/docs/es-menu-map.md"
git init -q -b main "${S}/es"; mkdir -p "${S}/es/es-app/src/guis"
cat > "${S}/es/es-app/src/guis/GuiMenu.cpp" <<'CPP'
void a(Window* window) {
	auto s = new GuiSettings(window, _("SYSTEM SETTINGS"));
}
void b(Window* window, bool backup) {
	auto s = new GuiSettings(window, backup ? _("CONTENT TO BACK UP") : _("CONTENT TO RESTORE"));
}
CPP
git -C "${S}/es" -c user.name=t -c user.email=t@t -c core.hooksPath=/dev/null add -A
git -C "${S}/es" -c user.name=t -c user.email=t@t -c core.hooksPath=/dev/null commit -q -m es
python3 -I "${S}/r/tools/es-menu-map-check" --es-src "${S}/es" --ref HEAD > "${S}/out" 2>&1; rc=$?
check "the literal-titled page is mapped and the exit is unchanged: 0 (rc ${rc})" '[ "${rc}" -eq 0 ]'
check "the computed-titled page is reported as unchecked, by file and line" 'grep -q "UNCHECKED  GuiMenu.cpp:5" "${S}/out"'
check "the summary counts it" 'grep -q "1 page(s) with a computed title" "${S}/out"'
if [ "${fail}" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
