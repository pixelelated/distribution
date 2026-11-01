#!/bin/bash
# T37 (#684): the recipe slice's checker, the brief's § 5 item 3 in eight steps.
#   t37-checks.sh --tree <scratch export> --repo <worktree> --commit <hash> --expect-es-pin <40 hex>
#                 --devices "GENERIC_X64:x86_64 H700:aarch64" --out <scratch dir> [--compare <stamps.txt>]
# --tree is a scratch export (git archive | tar -x), never a checkout: every sourced-recipe call runs
# there under env -i with HOME in scratch (ruling (k)); --repo is read with git only. Each assertion
# prints PASS, FAIL or WARN with its step and name, never a recipe line's text (:39 of the ES recipe is
# never printed); the last line is TOTAL. Exit 0 all PASS (WARN allowed), 1 any FAIL, 2 nothing checked
# (a refusal: no tree, no config/options, a .git in the tree, an --out outside /workspace/tmp, a
# missing bash, python3 or git).
set -u
TREE= REPO= COMMIT= PIN= DEVICES= OUT= COMPARE=
while [ $# -gt 0 ]; do
  case "$1" in
    --tree) TREE=$2; shift 2;; --repo) REPO=$2; shift 2;; --commit) COMMIT=$2; shift 2;;
    --expect-es-pin) PIN=$2; shift 2;; --devices) DEVICES=$2; shift 2;; --out) OUT=$2; shift 2;;
    --compare) COMPARE=$2; shift 2;; *) echo "REFUSED: unknown argument $1 -- nothing checked"; exit 2;;
  esac
done
refuse() { echo "REFUSED: $1 -- nothing checked"; exit 2; }
for t in bash python3 git find sha256sum; do command -v "$t" >/dev/null || refuse "$t missing"; done
[ -n "$TREE" ] && [ -d "$TREE" ] || refuse "no --tree"
[ -f "$TREE/config/options" ] || refuse "no config/options in --tree"
[ -e "$TREE/.git" ] && refuse "--tree holds a .git (a git worktree, ruling (k))"
[ -n "$REPO" ] && git -C "$REPO" rev-parse --verify -q "${COMMIT}^{commit}" >/dev/null || refuse "--repo/--commit unreadable"
[[ "$PIN" =~ ^[0-9a-f]{40}$ ]] || refuse "--expect-es-pin is not 40 hex"
[ -n "$DEVICES" ] || refuse "no --devices"
case "$OUT" in /workspace/tmp/*) ;; *) refuse "--out is not under /workspace/tmp (HOME must be scratch)";; esac
mkdir -p "$OUT/home" || refuse "--out not writable"
TREE=$(cd "$TREE" && pwd); U=projects/ROCKNIX/packages/ui
NAMES="emulationstation es-theme-art-book-next lowerdeck"
P=0; N=0
pass() { P=$((P+1)); N=$((N+1)); echo "PASS step $1 $2${3:+: $3}"; }
fail() { N=$((N+1)); echo "FAIL step $1 $2${3:+: $3}"; }
warn() { echo "WARN step $1 $2${3:+: $3}"; }
check() { local s=$1 n=$2 ok=$3 d=${4:-}; if [ "$ok" = 1 ]; then pass "$s" "$n" "$d"; else fail "$s" "$n" "$d"; fi; }

# (1) the inventory: the tree's ui/ names against the commit's, and the commit's count and ui/ tree hash
git -C "$REPO" ls-tree -r --name-only "$COMMIT" -- "$U/" | LC_ALL=C sort > "$OUT/inv-commit.txt"
(cd "$TREE" && find "$U" -type f | LC_ALL=C sort) > "$OUT/inv-tree.txt"
n_c=$(wc -l < "$OUT/inv-commit.txt"); th=$(git -C "$REPO" rev-parse "$COMMIT:$U")
delta=$(LC_ALL=C comm -3 "$OUT/inv-commit.txt" "$OUT/inv-tree.txt" | tr -d '\t' | tr '\n' ' ')
check 1 inventory-count "$([ "$n_c" = 19 ] && echo 1 || echo 0)" "$n_c at the commit, ui/ tree $th"
check 1 inventory-names "$([ -z "$delta" ] && echo 1 || echo 0)" "${delta:-the tree's names equal the commit's}"

# (2) bash -n on the seven
for f in emulationstation/package.mk lowerdeck/package.mk themes/es-theme-art-book-next/package.mk \
         emulationstation/sources/es_settings emulationstation/sources/start_es.sh \
         emulationstation/sources/serial_number_check emulationstation/autostart/001-emulationstation; do
  if [ -s "$TREE/$U/$f" ]; then bash -n "$TREE/$U/$f" 2>/dev/null; rc=$?; else rc=99; fi
  check 2 "bash-n $f" "$([ $rc = 0 ] && echo 1 || echo 0)" "rc=$rc"
done

# (3) one recipe per name, then tools/pkgcheck by name in the tree (and the control)
for nm in $NAMES; do
  c=$(cd "$TREE" && find packages projects -type f -path "*/$nm/package.mk" | wc -l)
  check 3 "find $nm" "$([ "$c" = 1 ] && echo 1 || echo 0)" "$c match"
  (cd "$TREE" && tools/pkgcheck "$nm") > "$OUT/pkgcheck-$nm.txt" 2>&1; rc=$?
  f=$(grep -c -a 'FAIL' "$OUT/pkgcheck-$nm.txt"); w=$(grep -c -a 'WARN' "$OUT/pkgcheck-$nm.txt")
  check 3 "pkgcheck $nm" "$([ $rc = 0 ] && [ "$f" = 0 ] && echo 1 || echo 0)" "rc=$rc FAIL-lines=$f WARN-lines=$w"
done
c=$(cd "$TREE" && find packages projects -type f -path "*/es-theme-no-such-package/package.mk" | wc -l)
check 3 "control es-theme-no-such-package" "$([ "$c" = 0 ] && echo 1 || echo 0)" "$c match (pkgcheck would pass it vacuously, L-21)"

# (4) the sourced-recipe assertions per device, in the tree, under env -i; (7) the stamps from the same call
: > "$OUT/fields.txt"; : > "$OUT/stamps.txt"
for dv in $DEVICES; do for nm in $NAMES; do
  env -i HOME="$OUT/home" PATH=/usr/bin:/bin PROJECT=ROCKNIX DEVICE="${dv%%:*}" ARCH="${dv##*:}" bash -c '
    cd "$1" || exit 2; . config/options "$2" >/dev/null 2>&1 || { echo "SOURCE_FAILED=1"; exit 0; }
    if [ "${TARGET_ARCH}" = "x86_64" ]; then pa=x86; elif [ "${PKG_IS_KERNEL_PKG}" = "yes" ]; then pa="${TARGET_KERNEL_PATCH_ARCH:-${TARGET_ARCH}}"; else pa="${TARGET_PATCH_ARCH:-${TARGET_ARCH}}"; fi
    reach="${PKG_DIR}/patches ${PKG_DIR}/patches/${pa} ${PKG_DIR}/patches/${PKG_VERSION} ${PKG_DIR}/patches/${PKG_VERSION}/${pa} ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME} ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${pa} ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/${PKG_VERSION} ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}"
    for d in ${PKG_PATCH_DIRS}; do case "$d" in /*) reach+=" $d";; *) reach+=" ${PKG_DIR}/patches/$d ${PROJECT_DIR}/${PROJECT}/patches/${PKG_NAME}/$d ${PROJECT_DIR}/${PROJECT}/devices/${DEVICE}/patches/${PKG_NAME}/$d";; esac; done
    empty=; raw=$(sed -n "s/^PKG_DEPENDS_TARGET=//p" "$PKG_DIR/package.mk" | head -n 1)
    for v in $(printf "%s\n" "$raw" | grep -o -E "\\$\\{[A-Za-z_][A-Za-z0-9_]*\\}" | tr -d "\${}"); do [ -n "${!v:-}" ] || empty+=" $v"; done
    unres=; for w in ${PKG_NEED_UNPACK}; do [ -d "$w" ] || [ -d "$1/$w" ] || unres+=" $w"; done
    printf "PKG_DIR_REL=%s\n" "${PKG_DIR#$1/}"
    printf "PKG_VERSION=%s\nPKG_URL=%s\nPKG_SHA256=%s\nPATCH_ARCH=%s\nPKG_PATCH_DIRS=%s\n" "$PKG_VERSION" "$PKG_URL" "$PKG_SHA256" "$pa" "$PKG_PATCH_DIRS"
    printf "GLES3=%s\nRUNTIME_LOGIN=%s\n" "$(case " $PKG_CMAKE_OPTS_TARGET " in *" -DGLES3=1 "*) echo 1;; *) echo 0;; esac)" "$(case " $PKG_CMAKE_OPTS_TARGET " in *" -DSCREENSCRAPER_RUNTIME_DEV_LOGIN=1 "*) echo 1;; *) echo 0;; esac)"
    printf "EMPTY_EXPANSIONS=%s\nUNRESOLVED_NEED_UNPACK=%s\n" "${empty# }" "${unres# }"
    for r in $reach; do printf "REACH=%s\n" "${r#$1/}"; done
    printf "STAMP=%s\n" "$(calculate_stamp)"' _ "$TREE" "$nm" > "$OUT/f-${dv%%:*}-$nm.txt" 2>&1
  sed "s#^#${dv%%:*} $nm #" "$OUT/f-${dv%%:*}-$nm.txt" >> "$OUT/fields.txt"
  echo "${dv%%:*} $nm $(sed -n 's/^STAMP=//p' "$OUT/f-${dv%%:*}-$nm.txt")" >> "$OUT/stamps.txt"
done; done
field() { sed -n "s/^$1 $2 $3=//p" "$OUT/fields.txt" | head -n 1; }
for dv in $DEVICES; do d=${dv%%:*}
  for nm in $NAMES; do
    check 4 "$d $nm sourced" "$(grep -q "^$d $nm SOURCE_FAILED=1" "$OUT/fields.txt" && echo 0 || echo 1)"
    e=$(field "$d" "$nm" EMPTY_EXPANSIONS); check 4 "$d $nm depends-no-empty-expansion" "$([ -z "$e" ] && echo 1 || echo 0)" "${e:+empty: $e}"
  done
  v=$(field "$d" emulationstation PKG_VERSION)
  check 4 "$d emulationstation pin" "$([ "$v" = "$PIN" ] && [[ "$v" =~ ^[0-9a-f]{40}$ ]] && echo 1 || echo 0)" "${#v} chars, equal-to-expected=$([ "$v" = "$PIN" ] && echo yes || echo no)"
  u=$(field "$d" emulationstation PKG_URL); check 4 "$d emulationstation url" "$(case "$u" in https://github.com/pixelelated/*) echo 1;; *) echo 0;; esac)"
  for nm in es-theme-art-book-next lowerdeck; do s=$(field "$d" "$nm" PKG_SHA256)
    check 4 "$d $nm sha256" "$([[ "$s" =~ ^[0-9a-f]{64}$ ]] && echo 1 || echo 0)" "${#s} chars"; done
  check 4 "$d emulationstation -DGLES3=1" "$(field "$d" emulationstation GLES3)"
  check 4 "$d emulationstation -DSCREENSCRAPER_RUNTIME_DEV_LOGIN=1" "$(field "$d" emulationstation RUNTIME_LOGIN)"
  echo "INFO step 4 $d PATCH_ARCH=$(field "$d" emulationstation PATCH_ARCH) PKG_PATCH_DIRS=[$(field "$d" emulationstation PKG_PATCH_DIRS)]"
done
for nm in $NAMES; do
  rel=$(sed -n "s/^[^ ]* $nm PKG_DIR_REL=//p" "$OUT/fields.txt" | head -n 1)
  [ -d "$TREE/$rel/patches" ] || { echo "INFO step 4 $nm has no patches/ directory"; continue; }
  for pd in $(cd "$TREE" && find "$rel/patches" -name '*.patch' -printf '%h\n' | LC_ALL=C sort -u); do
    hit=$(grep -c -x -F "REACH=$pd" <(sed -n "s/^[^ ]* $nm //p" "$OUT/fields.txt"))
    check 4 "patch-dir-reached ${pd#$rel/}/ ($nm)" "$([ "$hit" -gt 0 ] && echo 1 || echo 0)" "reached for $hit of the listed devices"
  done
done

# (5) the install-text assertions over makeinstall_target and post_install, line numbers only
python3 -B -I - "$TREE/$U" > "$OUT/install-text.txt" <<'PY'
import re, sys, pathlib
base = pathlib.Path(sys.argv[1])
for rel in ("emulationstation/package.mk", "themes/es-theme-art-book-next/package.mk", "lowerdeck/package.mk"):
    lines = (base / rel).read_text().split("\n")
    fn = None; buf = []; start = None
    joined = []
    for i, l in enumerate(lines, 1):
        if fn is None:
            m = re.match(r"^(makeinstall_target|post_install)\(\)\s*\{", l)
            if m: fn = m.group(1); joined = []
            continue
        if l.startswith("}"):
            body = joined; fn_name = fn; fn = None
            links, rms, fills = [], [], []
            for n, t in body:
                s = t.strip()
                if s.startswith("#"): continue
                toks = s.split()
                if toks[:1] == ["ln"]:
                    args = [x for x in toks[1:] if not x.startswith("-")]
                    if args and args[0].startswith("${INSTALL}"): links.append(n)
                if toks[:1] == ["rm"]:
                    for x in toks[1:]:
                        if not x.startswith("-"): rms.append((n, x))
                if toks[:2] == ["mkdir", "-p"] and len(toks) > 2: fills.append((n, toks[2]))
                if toks[:1] == ["cp"] and len(toks) > 2: fills.append((n, toks[-1]))
                if re.search(r"\|\|\s*true\s*$", s): print(f"ORTRUE {rel}:{n} {fn_name}")
            for n in links: print(f"INSTALL_LINK {rel}:{n} {fn_name}")
            for n, p in rms:
                for m, d in fills:
                    if m > n and p.startswith(d.rstrip("/") + "/"):
                        print(f"RM_BEFORE_FILL {rel}:{n} {fn_name} (filled at :{m})"); break
            continue
        if joined and joined[-1][1].rstrip().endswith("\\"):
            joined[-1] = (joined[-1][0], joined[-1][1].rstrip()[:-1] + " " + l.strip())
        else:
            joined.append((i, l))
    if rel.startswith("emulationstation/"):
        txt = "\n".join(lines)
        if "emulationstation2.mo" not in txt: print(f"NO_CATALOG_GUARD {rel}")
PY
rc=$?; check 5 install-text-parsed "$([ $rc = 0 ] && echo 1 || echo 0)" "rc=$rc"
il=$(grep '^INSTALL_LINK' "$OUT/install-text.txt" | cut -d' ' -f2 | tr '\n' ' ')
check 5 "no-link-to-\${INSTALL}-target (L-03)" "$([ -z "$il" ] && echo 1 || echo 0)" "${il:+at $il}"
rb=$(grep '^RM_BEFORE_FILL' "$OUT/install-text.txt" | cut -d' ' -f2- | tr '\n' ' ')
check 5 "no-rm-before-its-directory-is-filled (L-04)" "$([ -z "$rb" ] && echo 1 || echo 0)" "${rb:+at $rb}"
for d in $DEVICES; do d=${d%%:*}; un=$(field "$d" emulationstation UNRESOLVED_NEED_UNPACK)
  check 5 "$d PKG_NEED_UNPACK-words-are-directories (L-19)" "$([ -z "$un" ] && echo 1 || echo 0)" "${un:+unresolved: $un}"; done
for l in $(grep '^ORTRUE' "$OUT/install-text.txt" | cut -d' ' -f2); do warn 5 "or-true (L-07)" "$l"; done
grep -q '^NO_CATALOG_GUARD' "$OUT/install-text.txt" && warn 5 "french-catalog-not-asserted (L-08)" "no line of the ES recipe names emulationstation2.mo"

# (6) the text checks over the slice's files: non-ASCII, the hooks' secret patterns, forbidden terms, XML
(cd "$TREE" && find "$U" -type f -not -path '*/patches/*' | LC_ALL=C sort) > "$OUT/slice.txt"
check 6 slice-count "$([ "$(wc -l < "$OUT/slice.txt")" = 15 ] && echo 1 || echo 0)" "$(wc -l < "$OUT/slice.txt") files"
na=$(printf 'x\xc3\xa9x\n' | LC_ALL=C grep -c -P '[^\x00-\x7F]')
check 6 planted-non-ascii-positive "$([ "$na" = 1 ] && echo 1 || echo 0)"
nf=; while read -r f; do c=$(LC_ALL=C grep -c -P '[^\x00-\x7F]' "$TREE/$f"); [ "$c" -gt 0 ] && nf+=" ${f#$U/}"; done < "$OUT/slice.txt"
check 6 non-ascii-files "$([ -z "$nf" ] && echo 1 || echo 0)" "${nf:+in$nf}"
SECRET_PATTERNS=; . "$REPO/.githooks/secret-patterns"; printf '' | grep -E -e "$SECRET_PATTERNS" >/dev/null 2>&1; crc=$?
check 6 secret-patterns-compile "$([ -n "$SECRET_PATTERNS" ] && [ $crc -le 1 ] && echo 1 || echo 0)" "rc=$crc"
pl=$(printf '%s\n' "$(printf -- '-----BEGIN %s-----' 'OPENSSH PRIVATE KEY')" | grep -c -E -e "$SECRET_PATTERNS")
check 6 planted-secret-positive "$([ "$pl" = 1 ] && echo 1 || echo 0)"
sf=; while read -r f; do c=$(grep -c -E -e "$SECRET_PATTERNS" "$TREE/$f"); [ "$c" -gt 0 ] && sf+=" ${f#$U/}"; done < "$OUT/slice.txt"
check 6 secret-pattern-files "$([ -z "$sf" ] && echo 1 || echo 0)" "${sf:+in$sf}"
echo "a planted forbidden-term line" | FORBIDDEN_PATTERNS='planted forbidden-term' "$REPO/tools/forbidden-terms-check" --stdin >/dev/null 2>&1; prc=$?
check 6 planted-forbidden-positive "$([ $prc = 1 ] && echo 1 || echo 0)" "rc=$prc"
(while read -r f; do cat "$TREE/$f"; done < "$OUT/slice.txt") | "$REPO/tools/forbidden-terms-check" --stdin >/dev/null 2>&1; frc=$?
check 6 forbidden-terms "$([ $frc = 0 ] && echo 1 || echo 0)" "rc=$frc"
for c in $(grep -E '\.cfg$' "$OUT/slice.txt"); do
  python3 -B -I -c 'import sys,xml.etree.ElementTree as E; E.parse(sys.argv[1])' "$TREE/$c" 2>/dev/null; rc=$?
  check 6 "xml ${c#$U/}" "$([ $rc = 0 ] && echo 1 || echo 0)"; done

# (7) the stamps; with --compare, each changed stamp belongs to a package whose directory differs from
# the commit, and every such package's stamp moved
check 7 stamps-written "$([ "$(grep -c -E ' [0-9a-f]{64}$' "$OUT/stamps.txt")" = "$(wc -l < "$OUT/stamps.txt")" ] && [ -s "$OUT/stamps.txt" ] && echo 1 || echo 0)" "$(wc -l < "$OUT/stamps.txt") stamps"
if [ -n "$COMPARE" ]; then
  touched=; for nm in $NAMES; do rel=$(sed -n "s/^[^ ]* $nm PKG_DIR_REL=//p" "$OUT/fields.txt" | head -n 1)
    a=$(git -C "$REPO" ls-tree -r "$COMMIT" -- "$rel/" | awk '{print $4, $3}' | LC_ALL=C sort)
    b=$(cd "$TREE" && find "$rel" -type f -not -name '.*' | LC_ALL=C sort | while read -r f; do echo "$f $(git hash-object "$f")"; done)
    [ "$a" = "$b" ] || touched+=" $nm"; done
  for dv in $DEVICES; do d=${dv%%:*}; for nm in $NAMES; do
    old=$(sed -n "s/^$d $nm //p" "$COMPARE"); new=$(sed -n "s/^$d $nm //p" "$OUT/stamps.txt")
    moved=$([ "$old" != "$new" ] && echo 1 || echo 0); t=$(case " $touched " in *" $nm "*) echo 1;; *) echo 0;; esac)
    check 7 "$d $nm stamp-moves-iff-touched" "$([ "$moved" = "$t" ] && echo 1 || echo 0)" "moved=$moved touched=$t"
  done; done
fi
echo "TOTAL: $P of $N assertions"
[ "$P" = "$N" ] && exit 0 || exit 1
