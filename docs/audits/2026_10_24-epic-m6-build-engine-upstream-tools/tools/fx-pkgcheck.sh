#!/usr/bin/env bash
# T6 (#653): tools/pkgcheck, from a commit or the working tree, run over a
# fixture tree of two recipes in the scratch directory given (pkgcheck reads
# recipes and prints; it writes nothing). Cases: a clean recipe, a recipe with
# a global-scope ${PKG_BUILD} (the positive control), and a name that matches
# no recipe.
#   fx-pkgcheck.sh <scratch-dir> [commit|WORKTREE]
set -u
S="${1:?scratch directory}"; R="${2:-8ebaf8daad}"
REPO="$(git rev-parse --show-toplevel)"
W="$S/fx-pkgcheck-$(date +%s%N)"; mkdir -p "$W/packages/fixture/fixturegood" "$W/packages/fixture/fixturebad" "$W/projects"
if [ "$R" = WORKTREE ]; then cp "$REPO/tools/pkgcheck" "$W/pkgcheck"; else git -C "$REPO" show "$R:tools/pkgcheck" > "$W/pkgcheck"; fi
printf 'PKG_NAME="fixturegood"\nPKG_VERSION="1"\n\nmakeinstall_target() {\n  cp ${PKG_BUILD}/x ${INSTALL}\n}\n' > "$W/packages/fixture/fixturegood/package.mk"
printf 'PKG_NAME="fixturebad"\nPKG_VERSION="1"\nPKG_FIXTURE="${PKG_BUILD}/x"\n' > "$W/packages/fixture/fixturebad/package.mk"
cd "$W"
for arg in fixturegood fixturebad fixture-no-such-package; do
  out=$(env -i PATH=/usr/bin:/bin TERM=dumb bash ./pkgcheck "$arg" 2>/dev/null); rc=$?
  echo "pkgcheck $arg: exit $rc; FAIL lines $(grep -c 'FAIL' <<<"$out"); recipes named $(grep -c 'package.mk' <<<"$out")"
done
