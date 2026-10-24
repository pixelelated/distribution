#!/bin/bash
# calculate_stamp sandbox (#652): a fixture override sourcing its generic twin.
D=/workspace/repos/pixelelated/distribution.worktrees/m6-build-engine-652
SB=${1:?usage: sb-calculate-stamp.sh <empty scratch dir>}; mkdir -p "$SB"; SB=$(cd "$SB" && pwd)
F=$SB/tree
rm -rf "$F"; mkdir -p "$F/packages/devel/fixturepkg" "$F/projects/ROCKNIX/packages/devel/fixturepkg" "$F/plain/packages/devel/plainpkg"
printf 'PKG_NAME="fixturepkg"\nPKG_VERSION="1.0"\n' > "$F/packages/devel/fixturepkg/package.mk"
printf '. ${ROOT}/packages/devel/fixturepkg/package.mk\npost_unpack() { :; }\n' > "$F/projects/ROCKNIX/packages/devel/fixturepkg/package.mk"
cat > "$SB/cache_global" <<C
$F/packages/devel/fixturepkg@?+?@
C
. "$D/config/functions"
stamp_of() {
  ( cd "$F" && ROOT="$F" PROJECT_DIR="$F/projects" PROJECT=ROCKNIX DEVICE=H700 PKG_NAME=fixturepkg \
    PKG_DIR="$F/projects/ROCKNIX/packages/devel/fixturepkg" PKG_NEED_UNPACK= PKG_STAMP= \
    _CACHE_PACKAGE_GLOBAL="$SB/cache_global" calculate_stamp )
}
a=$(stamp_of); echo "stamp before: $a"
printf 'PKG_NAME="fixturepkg"\nPKG_VERSION="1.1"\n' > "$F/packages/devel/fixturepkg/package.mk"
b=$(stamp_of); echo "stamp after the generic recipe's bump: $b"
[ "$a" != "$b" ] && echo "RESULT: the stamp moved" || echo "RESULT: the stamp did not move"
# control: the same computation with the global directory lookup disabled (the pre-cb884edb0f behaviour)
get_global_pkg_directory() { :; }
c=$(stamp_of)
printf 'PKG_NAME="fixturepkg"\nPKG_VERSION="1.2"\n' > "$F/packages/devel/fixturepkg/package.mk"
e=$(stamp_of)
[ "$c" != "$e" ] && echo "CONTROL: moved without the lookup" || echo "CONTROL: without the global lookup the stamp does not move (the pre-fix shape)"
