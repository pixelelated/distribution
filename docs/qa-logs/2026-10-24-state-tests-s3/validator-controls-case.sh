#!/bin/bash
# validator-controls-case.sh -- T14 S3's control for #994: does each of the
# validator's rewritten controls catch the product defect it is named for?
# Four product mutations, each in a scratch root (the rclone sources and the
# recipe copied, then changed), each run with --case against two validators:
# the stage-D one (its version literal patched, the only change, so it can run
# against the package's rclone) and the fixed one. For the timeout, the
# stage-D listing never fails, so the comparison is the fixed tool with its
# elapsed check reverted. Nothing outside the scratch.
#   validator-controls-case.sh <tree> <stage-D tools dir> <rclone> <scratch>
set -u
T="$(cd "$1" && pwd)"; OLD="$(cd "$2" && pwd)"; RC="$3"; S="$4"; rm -rf "$S"; mkdir -p "$S"
SRC=projects/ROCKNIX/packages/network/rclone
BT=projects/ROCKNIX/packages/rocknix/sources/scripts
fail=0
check() { if [ "$2" = 0 ]; then echo "  ok    $1"; else echo "  FAIL  $1"; fail=1; fi; }
root() {  # <dir> <validator source>: a scratch root with the two tools and the rclone package
  mkdir -p "$1/tools" "$1/$SRC" "$1/$BT"; cp -r "$T/$SRC/sources" "$T/$SRC/package.mk" "$1/$SRC/"; cp "$T/$BT/backuptool" "$1/$BT/"
  sed "s/rclone v1\.75\.1'/rclone v1.75.2'/" "$2" > "$1/tools/pixelelated-cloud-validator-test"
  cp "$T/tools/rasteratops-cloud-layout-test" "$1/tools/"
}
mutate() {  # <dir> <mutation>
  v="$1/$SRC/sources/cloud_folder_validate"; c="$1/$SRC/sources/cloud_setup"
  case "$2" in
    empty) python3 -I - "$v" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read(); a="    print(json.dumps(result, separators=(',', ':')))"
assert a in s; open(p,'w').write(s.replace(a,"    if len(result['categories']) == 5: result['categories'] = []\n"+a))
PY
    ;;
    seed) sed -i 's#^\( *\)--seed-folders)$#&\n\1    [ "${2:-}" = roms ] \&\& exit 0#' "$c"; grep -q '\[ "${2:-}" = roms \] && exit 0' "$c" || { echo "seed mutation did not apply"; exit 2; } ;;
    bytes) sed -i 's/^MAX_BYTES = 2 \* 1024 \* 1024$/MAX_BYTES = 64 * 1024 * 1024/' "$v"; grep -q '^MAX_BYTES = 64' "$v" || { echo "bytes mutation did not apply"; exit 2; } ;;
    time) sed -i -e 's/def command(args, deadline, seconds=6,/def command(args, deadline, seconds=60,/' -e 's/^TOTAL_SECONDS = 25$/TOTAL_SECONDS = 120/' "$v"; grep -q 'seconds=60' "$v" || { echo "time mutation did not apply"; exit 2; } ;;
  esac
}
revert_elapsed() { python3 -I - "$1/tools/pixelelated-cloud-validator-test" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read()
a="        require(elapsed < 12, f'the request took {elapsed:.1f} s: the listing was not cut short')"
assert a in s; open(p,'w').write(s.replace(a,"        pass"))
PY
}
run() { python3 -I "$1/tools/pixelelated-cloud-validator-test" --rclone "$RC" --output "$1/out" --case "$2" > "$1/run.txt" 2>&1; echo $?; }
for m in empty:populated-read-only seed:explicit-category-seeding bytes:byte-limit time:request-timeout; do
  mut=${m%%:*}; case_=${m#*:}
  old="$S/$mut-old"; root "$old" "$OLD/pixelelated-cloud-validator-test"; mutate "$old" "$mut"
  [ "$mut" = time ] && { root "$old" "$T/tools/pixelelated-cloud-validator-test"; mutate "$old" "$mut"; revert_elapsed "$old"; }
  new="$S/$mut-new"; root "$new" "$T/tools/pixelelated-cloud-validator-test"; mutate "$new" "$mut"
  ro=$(run "$old" "$case_"); rn=$(run "$new" "$case_")
  echo "  $mut ($case_): the $([ "$mut" = time ] && echo 'state-only' || echo 'stage-D') control rc $ro | the fixed control rc $rn | $(tail -1 "$new/run.txt" | cut -c1-90)"
  check "the $([ "$mut" = time ] && echo 'state-only' || echo 'stage-D') control credits the $mut mutation (the positive)" "$([ "$ro" = 0 ] && echo 0 || echo 1)"
  check "the fixed control fails the $mut mutation" "$([ "$rn" != 0 ] && echo 0 || echo 1)"
done
if [ "$fail" -eq 0 ]; then echo PASS; else echo FAIL; exit 1; fi
