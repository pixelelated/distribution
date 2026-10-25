#!/bin/bash
# #1036, four of the five predicates in one clone. Must FAIL on the fixed file:
#   q: "the boot pass ran over" (the pass ends false; the unfixed read wait's 0)
#   q: "samba on: smb.conf is still there", "toggle on: raofflineproxy.conf is
#      still there" (the pass no longer rewrites its markers; the fixture's own stay)
#   t: "each compiled" (a patch adds a module that does not compile)
#   D21: "the four scripts under sources/ are mode 100755" (one is a symlink, 120000, in the index)
. "$(dirname "$0")/alter-lib.sh"
N="${R}/rocknix/autostart/099-networkservices"
echo false >> "${N}"; echo "  ${N#${C}/}:$(wc -l < "${N}"): appended 'false' (the pass's own status is 1)"
change "${N}" '^    rm -f "/storage/.cache/services/\$\{CONF\}"$' 's/^    rm -f "\/storage\/.cache\/services\/\$\{CONF\}"$/    : # T15 #1036: the marker is no longer removed/'
change "${N}" '^      touch "/storage/.cache/services/\$\{CONF\}"$' 's/^      touch "\/storage\/.cache\/services\/\$\{CONF\}"$/      : # T15 #1036: nor rewritten/'
P="${R}/network/raofflineproxy/patches/999-t15-1036-uncompilable.patch"
printf -- '--- /dev/null\n+++ b/linux/raofflineproxy/t15_1036_broken.py\n@@ -0,0 +1 @@\n+def (:\n' > "${P}"
echo "  ${P#${C}/}: a new patch adding a module that does not compile"
H="${R}/network/raofflineproxy/sources/raofflineproxy-refresh"
mv "${H}" "${H}.real"; ln -s raofflineproxy-refresh.real "${H}"; git -C "${C}" add -- "${H#${C}/}" "${H#${C}/}.real"
[ "$(git -C "${C}" ls-files -s -- "${H#${C}/}" | cut -c1-6)" = 120000 ] || { echo "alter: the index does not hold the symlink" >&2; exit 2; }
echo "  ${H#${C}/}: a symlink in the index (mode 120000), never committed"
