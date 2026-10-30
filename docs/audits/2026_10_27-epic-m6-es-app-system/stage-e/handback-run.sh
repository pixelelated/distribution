#!/bin/bash
# T33 (#680) stage E's hand-back: every stage-C and stage-E harness at the ES tip.
# Default runs are the positives (rc 0 expected); pl25 is the recorded lead
# (rc 1 expected, a FAIL at every commit until the rescan's owner fixes it);
# each --control on a fixed file is guarded CANNOT (rc 2).
#   bash stage-e/handback-run.sh   (after: . stage-a/env.sh)
set -u
cd "$(dirname "$0")/.."
S=${W:?}/es-app/src
VC=/workspace/tmp/m6-t33/pin/ViewController.cpp
PO=$W/locale/lang/fr/LC_MESSAGES/emulationstation2.po
unexpected=0
check() {   # expected-rc name command...
  local want=$1 name=$2; shift 2
  out=$("$@" 2>&1); rc=$?
  last=$(printf '%s\n' "$out" | grep -E '^(PASS|FAIL|CANNOT|SUMMARY)|rc |[0-9] tag names|direct post' | tail -1)
  [ "$rc" = "$want" ] && v=ok || { v=UNEXPECTED; unexpected=$((unexpected+1)); }
  printf '%-10s %-44s rc %s (want %s)  %s\n' "$v" "$name" "$rc" "$want" "${last:0:150}"
}
check 0 l06-collections        python3 -I stage-c/l06-collections.py $S/CollectionSystemManager.cpp $VC
check 0 l06-reload-collection  python3 -I stage-c/l06-reload-collection.py $S/CollectionSystemManager.cpp
check 2 "l06-reload-collection --control" python3 -I stage-c/l06-reload-collection.py $S/CollectionSystemManager.cpp --control
check 0 l07-search-builder     python3 -I stage-c/l07-search-builder.py $S/components/ScraperSearchComponent.cpp
check 2 "l07-search-builder --control" python3 -I stage-c/l07-search-builder.py $S/components/ScraperSearchComponent.cpp --control
check 0 l12-network-posts      python3 -I stage-c/l12-network-posts.py $S/NetworkThread.cpp $S/AppWindow.h
check 2 "l12-network-posts --control" python3 -I stage-c/l12-network-posts.py $S/NetworkThread.cpp $S/AppWindow.h --control
check 0 l309-rating-year       python3 -I stage-c/l309-rating-year.py $S/FileFilterIndex.cpp
check 0 l313-gamelist-merge    python3 -I stage-c/l313-gamelist-merge.py $S/Gamelist.cpp $S/MetaData.cpp $S/MetaData.h "$PUGIXML_INCLUDE_DIR" same desc default whole
check 0 l313-gamelist-save     python3 -I stage-c/l313-gamelist-save.py $S/Gamelist.cpp "$PUGIXML_INCLUDE_DIR"
check 0 l313-update-gamelist   python3 -I stage-c/l313-update-gamelist.py $S/Gamelist.cpp "$PUGIXML_INCLUDE_DIR"
check 2 "l313-update-gamelist --control" python3 -I stage-c/l313-update-gamelist.py $S/Gamelist.cpp "$PUGIXML_INCLUDE_DIR" --control
check 0 l321-keys-parse        python3 -I stage-c/l321-keys-parse.py $S "$RAPIDJSON_INCLUDE_DIR"
for c in typenum trignum targetobj actionstr chord; do
  check 0 "l321-keys-shapes $c" python3 -I stage-c/l321-keys-shapes.py $S "$RAPIDJSON_INCLUDE_DIR" $c
done
check 0 l329-filetag-words     python3 -I stage-c/l329-filetag-words.py $S/FileTag.cpp $PO
check 2 "l329-filetag-words --control" python3 -I stage-c/l329-filetag-words.py $S/FileTag.cpp $PO --control
check 0 l331-lang-india        python3 -I stage-c/l331-lang-india.py $S/LangParser.cpp
check 0 l335-textfit-floor     python3 -I stage-c/l335-textfit-floor.py $S/TextFit.h
check 0 s2-collection-files    python3 -I stage-c/s2-collection-files.py $S/CollectionSystemManager.cpp $S/FileFilterIndex.cpp
check 0 s3-tables              python3 -I stage-c/s3-tables.py $S/Genres.cpp $S/MetaData.cpp $S/FileFilterIndex.cpp
check 0 s4a-token-check        python3 -I stage-c/s4a-token-check.py $S
check 0 "s4a-token-check --tsan" python3 -I stage-c/s4a-token-check.py $S --tsan
check 0 s4b-cloudoffer         python3 -I stage-c/s4b-cloudoffer.py $S
check 0 s4b-writes             python3 -I stage-c/s4b-writes.py $S
check 0 s5-bluetooth           python3 -I stage-c/s5-bluetooth.py $S
check 1 "pl25-screensaver (the lead)" python3 -I stage-c/pl25-screensaver.py $S/SystemScreenSaver.cpp
echo "handback-run: $unexpected unexpected"
exit $((unexpected > 0))
