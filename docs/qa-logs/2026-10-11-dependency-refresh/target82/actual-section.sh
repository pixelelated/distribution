set -uo pipefail
ROOT=/workspace/repos/rocknix.worktrees/m7-component-inputs
F2=/workspace/tmp/pix541-f2-target82/fixture
OLD=0
BASE_REF=next
SOURCES_DIR=/workspace/cache/rocknix-sources
FAIL=0
check() { if [ "$1" -eq 0 ]; then echo "PASS $2"; else echo "FAIL $3"; FAIL=$((FAIL+1)); fi; }
echo "  F2-4. RetroArch's patches: the fork's apply at fuzz 0, the tree compiles, the sharp-size table follows the face that is drawn (#307 PL-032; #308 F-RW-02..10)"
RA_REL=projects/ROCKNIX/packages/emulators/libretro/retroarch
RA_PIN="$(sed -n 's/^PKG_VERSION="\([0-9a-f]*\)".*/\1/p' "${ROOT}/${RA_REL}/package.mk" | head -1)"
RA_TAR=""
for d in "${SOURCES_DIR:-}" /workspace/cache/rocknix-sources "${ROOT}/sources" "${ROOT}"/../*/sources; do
    [ -n "${d}" ] && [ -f "${d}/retroarch/retroarch-${RA_PIN}.tar.gz" ] && { RA_TAR="${d}/retroarch/retroarch-${RA_PIN}.tar.gz"; break; }
done
if [ -z "${RA_TAR}" ]; then
    # A check that cannot run has not passed (the audit of the fixes, claude
    # G-F2-10, gpt G-F2-06): with no pinned tree none of F2-4 runs, and the
    # run says so as a FAIL rather than a SKIP an aggregate PASSED hides.
    check 1 "" "retroarch-${RA_PIN:-?}.tar.gz is not under SOURCES_DIR, /workspace/cache/rocknix-sources or a build worktree's sources/ -- F2-4's eleven-plus checks did not run (an empty pin reads the same)"
else
RX="${F2}/ra"; mkdir -p "${RX}/patches/batteryplus" "${RX}/src"
if [ "${OLD}" -eq 1 ]; then
    git -C "${ROOT}" ls-tree --name-only "${BASE_REF}" "${RA_REL}/patches/" "${RA_REL}/patches/batteryplus/" | grep '\.patch$' \
      | while read -r f; do git -C "${ROOT}" show "${BASE_REF}:${f}" > "${RX}/patches/${f#${RA_REL}/patches/}"; done
else
    cp "${ROOT}/${RA_REL}"/patches/*.patch "${RX}/patches/"; cp "${ROOT}/${RA_REL}"/patches/batteryplus/*.patch "${RX}/patches/batteryplus/"
fi
tar -xzf "${RA_TAR}" -C "${RX}/src" --strip-components=1 --wildcards '*.h' '*.c' '*.cpp' '*/version.all' 2>/dev/null
# patch dry-runs spill large files; use this owned host fixture, not /tmp.
F2_FUZZ=""; F2_APPLY=0
for p in "${RX}"/patches/*.patch "${RX}"/patches/batteryplus/*.patch; do
    n="${p#${RX}/patches/}"
    # The fork's (0011-video-thread-*, 0013 and up) are tried at fuzz 0 first
    # and noted when that fails; every patch is then applied as the package
    # applies it, so the checks below read the tree the build would.
    case "${n}" in
        0011-video-thread-*|001[3-9]-*|00[2-9][0-9]-*)
            TMPDIR="${RX}" patch -d "${RX}/src" -p1 -N --fuzz=0 --dry-run -r - < "${p}" > "${RX}/fz.log" 2>&1 && ! grep -q 'with fuzz' "${RX}/fz.log" || F2_FUZZ+=" ${n}" ;;
    esac
    TMPDIR="${RX}" patch -d "${RX}/src" -p1 -N --no-backup-if-mismatch -r - < "${p}" > /dev/null 2>&1 || { F2_APPLY=1; F2_FUZZ+=" ${n}(FAILED)"; }
done
[ "${F2_APPLY}" -eq 0 ] && [ -z "${F2_FUZZ}" ]; check $? "every patch applies in the package's order, the fork's with no fuzz" "patches that needed fuzz or failed:${F2_FUZZ}"

fi
[ "$FAIL" -eq 0 ]
