#!/bin/bash
# T33 (#680) stage C: every host proof at the pin, then with its --control.
# The pin's sources are git show'n into /workspace/tmp/m6-t33/pin (<pin>).
# A sanitizer's long shadow dump is cut to its WARNING/SUMMARY/FAIL lines.
set -u
. "$(dirname "$0")/../stage-a/env.sh"
P=/workspace/tmp/m6-t33/pin/es-app/src; PO=/workspace/tmp/m6-t33/pin/fr.po
cd "$(dirname "$0")"
one() { local t; t=$(date -u +%H:%M:%SZ); echo "\$ python3 -I stage-c/$*    ($t)" | sed "s#$P#<pin>#g; s#$PO#<pin-fr.po>#; s#$RAPIDJSON_INCLUDE_DIR#<rapidjson>#; s#$PUGIXML_INCLUDE_DIR#<pugixml>#"
  python3 -I "$@" 2>&1 | grep -v -E '^\s*(0x[0-9a-f]+:|Shadow|  [A-Z][a-z].*: +[0-9a-f ]+$|==[0-9]+==ABORTING|#[0-9]+ 0x)' | sed -E 's#/workspace/tmp/m6-t33/tmp/[a-z0-9-]+/##g; s/(FAIL [a-z0-9-]+: rc [0-9]+).*/\1/' | head -20
  echo "rc=${PIPESTATUS[0]}"; echo; }
for c in "" --control; do
  one l309-rating-year.py $P/FileFilterIndex.cpp $c
  one l313-update-gamelist.py $P/Gamelist.cpp $PUGIXML_INCLUDE_DIR $c
  one l321-keys-parse.py $P $RAPIDJSON_INCLUDE_DIR $c
  one l329-filetag-words.py $P/FileTag.cpp $PO $c
  one l331-lang-india.py $P/LangParser.cpp $c
  one l335-textfit-floor.py $P/TextFit.h $c
  one l06-reload-collection.py $P/CollectionSystemManager.cpp $c
  one l07-search-builder.py $P/components/ScraperSearchComponent.cpp $c
  one l12-network-posts.py $P/NetworkThread.cpp $P/AppWindow.h $c
done
