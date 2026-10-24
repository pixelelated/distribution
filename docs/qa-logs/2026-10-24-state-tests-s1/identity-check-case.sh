#!/bin/bash
# identity-check-case.sh -- T14 S1's control for #990: rasteratops-identity-check
# over scratch trees exported from a commit, three ways -- the tree as it is,
# a Tools gamelist with no games, and an ES recipe whose second PKG_LICENSE
# overrides the first. Run for two tools (the stage-D one and the fixed one);
# each case reads the one check line it is about. Nothing outside the scratch.
#   identity-check-case.sh <repo> <commit> <tool> <es checkout at the pin> <scratch>
set -u
R="$(cd "$1" && pwd)"; C="$2"; TOOL="$(readlink -f "$3")"; ES="$4"; S="$5"; rm -rf "${S:?}"; mkdir -p "$S"
paths="distributions packages/linux projects/ROCKNIX/packages docs/pixelelated/art LICENSE.md TRADEMARK.md NAMING.md"
mk() { mkdir -p "$1"; git -C "$R" archive "$C" -- $paths | tar -x -C "$1"; }
line() { python3 -I "$TOOL" --tree "$1" --es "$ES" 2>&1 | grep -m1 -E "$2" | cut -c1-110; }
mk "$S/tree"
echo "  tree as is:      $(line "$S/tree" 'ES licence matches')"
mk "$S/empty"; printf '<?xml version="1.0"?>\n<gameList/>\n' > "$S/empty/projects/ROCKNIX/packages/misc/modules/sources/gamelist.xml"
echo "  empty gamelist:  $(line "$S/empty" 'Tools (metadata names its games|names and descriptions)')"
mk "$S/shadow"; f="$S/shadow/projects/ROCKNIX/packages/ui/emulationstation/package.mk"
sed -i 's/^PKG_LICENSE=.*/PKG_LICENSE="MIT"/' "$f"; printf 'PKG_LICENSE="GPL-2.0"\n' >> "$f"
echo "  shadowed licence: $(line "$S/shadow" 'ES licence matches')"
