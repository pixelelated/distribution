#!/bin/bash
# T18 (#665): the lines each new or contested seat item was graded at, at the
# pin (and the scripts at 8ebaf8daad), through the mask. Run from the
# distribution worktree; writes one file per item beside this script.
set -uo pipefail
W=/home/max/Development/emulationstation-next.worktrees/m6-es-cloud-pages-665
PIN=16dbac5211eea7e70db7394372033be2be7df829
O=docs/audits/2026_10_26-epic-m6-es-cloud-pages/stage-c/rereads
mask() { sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'; }
es() { git -C "$W" show "$PIN:$1" | sed -n "$2p" | awk -v s="${2%%,*}" '{printf "%5d  %s\n", NR+s-1, $0}' | mask; }
sc() { git show "8ebaf8daad:$1" | sed -n "$2p" | awk -v s="${2%%,*}" '{printf "%5d  %s\n", NR+s-1, $0}' | mask; }
{ echo "== A-33 the card's sample after pclose, and the instance cleared later"; es es-app/src/ThreadedCloudSync.cpp 446,458; es es-app/src/ThreadedCloudSync.cpp 716,720; echo "-- the job's own check"; es es-app/src/CloudTransferJob.cpp 686,696; } > "$O/a33.out"
{ echo "== A-34 the late pid within the budget"; es es-app/src/ThreadedCloudSync.cpp 836,863; } > "$O/a34.out"
{ echo "== A-36 the row with a full stop, and the parser that strips it"; es es-app/src/CloudText.cpp 425,425; es es-app/src/CloudText.cpp 571,580; es es-app/src/CloudText.cpp 469,475; } > "$O/a36.out"
{ echo "== A-37 the why labelled with mUnitLabel, and the tier that does not clear it"; es es-app/src/CloudTransferJob.cpp 280,288; es es-app/src/CloudTransferJob.cpp 333,336; es es-app/src/CloudTransferJob.cpp 374,375; } > "$O/a37.out"
{ echo "== A-38 the composer, the page's word, the manual sync"; es es-app/src/guis/GuiMenu.cpp 5002,5007; es es-app/src/guis/GuiCloudTransfer.cpp 435,435; es es-app/src/guis/GuiMenu.cpp 6139,6141; echo "-- --error-on-no-transfer in the scripts at 8ebaf8daad: $(git grep -c -e '--error-on-no-transfer' 8ebaf8daad -- projects | wc -l) files"; } > "$O/a38.out"
{ echo "== A-40 the rows set without fitOneLine"; es es-app/src/guis/GuiCloudTransfer.cpp 56,56; es es-app/src/guis/GuiCloudTransfer.cpp 913,915; es es-app/src/guis/GuiCloudTransfer.cpp 936,939; es es-app/src/guis/GuiCloudTransfer.cpp 1035,1035; } > "$O/a40.out"
{ echo "== A-15 whyForCode against why_for (codes 6 and 10)"; es es-app/src/ThreadedCloudSync.cpp 80,96; sc projects/ROCKNIX/packages/network/rclone/sources/cloud_backup 828,846; } > "$O/a15.out"
{ echo "== A-14 backuptool's why before its fail"; sc projects/ROCKNIX/packages/rocknix/sources/scripts/backuptool 1493,1497; } > "$O/a14.out"
echo "rereads written: $(ls "$O"/*.out | wc -l)"
