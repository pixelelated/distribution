#!/bin/bash
# T37 (#684): the checker's FAIL-first positive (the brief's § 5 item 3 step 8), for stage E's set
# (t37-streams.md § The rules, D-WORKFLOW-211). The fixed fixture is a scratch export of stage E's
# recipe tip (FIXAT, S1's five edits as committed) plus TWO FIXTURE-ONLY LINES -- PL-01's device link
# and PL-02's `PKG_PATCH_DIRS+=" x86_64"` -- so its exit-0 run holds. Those two are NOT T37's fixes:
# PL-01 is deferred to #613 and PL-02 to #1072 (rulings 2, 3, 12). The unfixed tip is a fresh export
# of the stage-D tip (TIPD). The fixture must pass and keep its stamps moving only for the package it
# touched; then one mutation at a time is applied to it, the checker run, and the mutation reverted
# (its file's sha256 checked back). Each mutation must exit 1 naming its assertion; the refusal case
# must exit 2. Credential-shaped text is assembled at run time. Prints one line per case and SUMMARY.
# Second run, 2026-11-01 03:2x UTC: two mutations added for the two stage-E assertions that had none
# (using-lines-print-no-value had only ever PASSed; armsx2-filter-matches-armsx2-turnip had FAILed at
# its parent but had no mutation). The first run's 18 lines are kept in stage-e/s1-failfirst.txt.
set -u
D=/workspace/repos/pixelelated/distribution.worktrees/m6-es-recipe-684
A=$D/docs/audits/2026_11_01-epic-m6-es-recipe; C=$A/tools/t37-checks.sh
FIXAT=c9e8d5a8df; TIPD=264a39f6d7; PIN=16dbac5211eea7e70db7394372033be2be7df829; DEV="GENERIC_X64:x86_64 H700:aarch64"
F=/workspace/tmp/m6-t37/fixed; O=/workspace/tmp/m6-t37/ff; U=projects/ROCKNIX/packages/ui; TX=/workspace/tmp/m6-t37/e/$TIPD
[ -e "$F" ] && { echo "STOP: $F exists"; exit 2; }
mkdir -p "$F" "$O"
( set -o pipefail; git -C "$D" archive "$FIXAT" | tar -x -C "$F" ) || { echo "STOP: export failed"; exit 2; }
[ -d "$TX/config" ] || { mkdir -p "$TX" && ( set -o pipefail; git -C "$D" archive "$TIPD" | tar -x -C "$TX" ) || { echo "STOP: tip export failed"; exit 2; }; }
E=$F/$U/emulationstation/package.mk
# the two fixture-only lines (not T37's fixes; #613 and #1072)
python3 -B -I - "$E" <<'PY2'
import sys
p = sys.argv[1]; s = open(p).read()
a = 'PKG_NEED_UNPACK="$(get_pkg_directory busybox)"\n'
assert s.count(a) == 1
s = s.replace(a, a + '[ "${ARCH}" = "x86_64" ] && PKG_PATCH_DIRS+=" x86_64"\n')
old = "ln -sf ${INSTALL}/usr/config/emulationstation/es_systems.cfg ${INSTALL}/etc/emulationstation/es_systems.cfg"
assert s.count(old) == 1
s = s.replace(old, "ln -sf /usr/config/emulationstation/es_systems.cfg ${INSTALL}/etc/emulationstation/es_systems.cfg")
open(p, "w").write(s)
PY2
[ $? = 0 ] || { echo "STOP: fixture edit failed"; exit 2; }
echo "fixture: $(git -C "$D" show "$FIXAT:$U/emulationstation/package.mk" | diff - "$E" | grep -c '^[<>]') changed lines in the ES recipe against $FIXAT (the two fixture-only lines)"
run() { bash "$C" --tree "$1" --repo "$D" --commit "$FIXAT" --expect-es-pin "$PIN" --devices "$DEV" --out "$O/$2" ${3:+--compare "$3"} > "$O/$2.out" 2>&1; echo $?; }
bash "$C" --tree "$TX" --repo "$D" --commit "$TIPD" --expect-es-pin "$PIN" --devices "$DEV" --out "$O/tip" > "$O/tip.out" 2>&1; trc=$?
echo "tip $TIPD (unfixed) exit=$trc $(tail -n 1 "$O/tip.out") fails: $(grep -c '^FAIL' "$O/tip.out")"
grep -E '^FAIL' "$O/tip.out" | sed 's/^/  tip: /'
frc=$(run "$F" fixed "$O/tip/stamps.txt"); echo "fixed fixture exit=$frc $(tail -n 1 "$O/fixed.out") fails: $(grep -c '^FAIL' "$O/fixed.out")"
grep -E '^(FAIL|WARN)|stamp-moves' "$O/fixed.out" | sed 's/^/  fixed: /'
caught=0; cases=0
mut() { # name, file, python-expression on s (the file text), the assertion the FAIL line must name
  local name=$1 file=$2 expr=$3 want=$4 sha0 rc ok
  cases=$((cases+1)); cp -p "$file" "$O/backup"; sha0=$(sha256sum < "$file")
  python3 -B -I -c 'import sys; p=sys.argv[1]; s=open(p).read(); exec(sys.argv[2]); open(p,"w").write(s)' "$file" "$expr"
  rc=$(run "$F" "m-$name")
  cp -p "$O/backup" "$file"; [ "$(sha256sum < "$file")" = "$sha0" ] || { echo "STOP: $name not reverted"; exit 2; }
  ok=0; [ "$rc" = 1 ] && grep -q -F -e "FAIL step" "$O/m-$name.out" && grep '^FAIL' "$O/m-$name.out" | grep -q -F -e "$want" && ok=1
  caught=$((caught+ok)); echo "mutation $name exit=$rc names [$want]: $([ $ok = 1 ] && echo CAUGHT || echo MISSED)"
}
SEC=$(printf -- '-----BEGIN %s-----' 'OPENSSH PRIVATE KEY')
mut global-pkg-build "$E" 's += "PKG_T37_PROBE=\"${PKG_BUILD}/x\"\n"' "pkgcheck emulationstation"
mut theme-sha-empty "$F/$U/themes/es-theme-art-book-next/package.mk" 'import re; s = re.sub(r"(?m)^PKG_SHA256=\"[0-9a-f]+\"", "PKG_SHA256=\"\"", s)' "es-theme-art-book-next sha256"
mut pin-abbreviated "$E" 'import re; s = re.sub(r"(?m)^PKG_VERSION=\"([0-9a-f]{10})[0-9a-f]+\"", lambda m: "PKG_VERSION=\"" + m.group(1) + "\"", s)' "emulationstation pin"
mut install-link "$E" 's = s.replace("  mkdir -p ${INSTALL}/etc\n", "  mkdir -p ${INSTALL}/etc\n    ln -sf ${INSTALL}/x ${INSTALL}/etc/x\n", 1)' "(L-03)"
mut rm-before-fill "$E" 's = s.replace("  mkdir -p ${INSTALL}/usr/config/emulationstation/resources\n", "    rm -f ${INSTALL}/usr/config/emulationstation/resources/logo.png\n  mkdir -p ${INSTALL}/usr/config/emulationstation/resources\n", 1)' "(L-04)"
mut bare-need-unpack "$E" 's = s.replace("PKG_NEED_UNPACK=\"$(get_pkg_directory busybox)\"", "PKG_NEED_UNPACK=\"busybox\"", 1)' "(L-19)"
mut url-elsewhere "$E" 's = s.replace("https://github.com/pixelelated/emulationstation", "https://github.com/elsewhere/emulationstation", 1)' "emulationstation url"
mut no-gles3 "$E" 's = s.replace("-DGLES3=1\"", "-DGLES2=1\"", 1)' "-DGLES3=1"
mut empty-expansion "$E" 's = s.replace("zstd ${OPENGLES}\"", "zstd ${OPENGLES} ${NO_SUCH_T37_VAR}\"", 1)' "depends-no-empty-expansion"
mut syntax-error "$F/$U/emulationstation/sources/serial_number_check" 's += "if then\n"' "bash-n emulationstation/sources/serial_number_check"
mut non-ascii "$F/$U/emulationstation/sources/start_es.sh" 's += "# " + chr(233) + "\n"' "non-ascii-files"
mut broken-xml "$F/$U/emulationstation/config/common/es_savestates.cfg" 's += "<unclosed>\n"' "xml emulationstation/config/common/es_savestates.cfg"
mut secret-line "$F/$U/emulationstation/sources/es_settings" "s += '# ' + '''$SEC''' + '\n'" "secret-pattern-files"
mut armsx2-block-removed "$E" 'import re; s, k = re.subn(r"\n  #ARMSX2.s own Turnip ships only on these devices \(see armsx2-sa\)\n  case \$\{DEVICE\} in\n.*?\n  esac\n", "\n", s, flags=re.S); assert k == 1' "armsx2-vulkan-driver-filter (L-01)"
mut catalog-guard-removed "$E" 'import re; s, k = re.subn(r"(?m)^    \[ -f \$\{INSTALL\}/usr/config/locale/fr/LC_MESSAGES/emulationstation2\.mo \][^\n]*\n", "", s); assert k == 1' "french-catalog-guard (L-08)"
mut hfs-removed "$E" 's = s.replace("CHEEVOS_DEV_LOGIN \\\n             HFS_DEV_LOGIN; do", "CHEEVOS_DEV_LOGIN; do", 1); assert "HFS_DEV_LOGIN; do" not in s' "using-lines-name-every-kept-credential (L-05)"
mut using-prints-value "$E" 's = s.replace("echo \"USING: ${key} (set)\"", "echo \"USING: ${key} (${!key})\"", 1); assert "(${!key})" in s' "using-lines-print-no-value (L-05)"
mut armsx2-list-differs "$E" 's = s.replace("    SM4450|SM6115|SM8250|SM8550|SM8650) ;;", "    SM4450|SM6115|SM8250|SM8550) ;;", 1); assert "SM8550|SM8650) ;;" not in s' "armsx2-filter-matches-armsx2-turnip (L-01)"
# a directory reached by no glob: added, run, removed
cases=$((cases+1)); mkdir -p "$F/$U/emulationstation/patches/nowhere"; printf '%s\n' '--- a/x' '+++ b/x' > "$F/$U/emulationstation/patches/nowhere/0001-t37-probe.patch"
rc=$(run "$F" m-patch-dir-nowhere); rm -r -- "${F:?}/$U/emulationstation/patches/nowhere"
ok=0; [ "$rc" = 1 ] && grep '^FAIL' "$O/m-patch-dir-nowhere.out" | grep -q -F 'patch-dir-reached patches/nowhere/' && ok=1; caught=$((caught+ok))
echo "mutation patch-dir-nowhere exit=$rc names [patch-dir-reached patches/nowhere/]: $([ $ok = 1 ] && echo CAUGHT || echo MISSED)"
# a stamp that moved without its package being touched: a doctored comparison file
cases=$((cases+1)); sed -E 's/^(GENERIC_X64 lowerdeck )[0-9a-f]{64}$/\1'"$(printf '0%.0s' $(seq 64))"'/' "$O/tip/stamps.txt" > "$O/stamps-doctored.txt"
rc=$(run "$F" m-stamp-doctored "$O/stamps-doctored.txt")
ok=0; [ "$rc" = 1 ] && grep '^FAIL' "$O/m-stamp-doctored.out" | grep -q -F 'GENERIC_X64 lowerdeck stamp-moves-iff-touched' && ok=1; caught=$((caught+ok))
echo "mutation stamp-doctored exit=$rc names [GENERIC_X64 lowerdeck stamp-moves-iff-touched]: $([ $ok = 1 ] && echo CAUGHT || echo MISSED)"
# the refusal: a tree holding a .git
mkdir "$F/.git"; rc=$(run "$F" refusal-git); rmdir "$F/.git"
echo "refusal git-tree exit=$rc: $([ "$rc" = 2 ] && grep -q '^REFUSED' "$O/refusal-git.out" && echo REFUSED-AS-REQUIRED || echo NOT-REFUSED)"
frc2=$(run "$F" fixed-again "$O/tip/stamps.txt"); echo "fixed fixture again exit=$frc2 $(tail -n 1 "$O/fixed-again.out")"
echo "SUMMARY: tip exit $trc; fixed fixture exit $frc then $frc2; $caught of $cases mutations caught; refusal exit $rc"
