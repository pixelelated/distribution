#!/bin/bash
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
# Copied for M6 T30 (#677) from T3's docs/audits/2026_10_24-epic-m6-emulators-libretro/tools/q4c-patches.sh at b3cb4ec8c5
# (feature/m6-emulators-libretro-650); T30's changes, if any, are named below.
#
# q4c-patches.sh -- RetroArch's patch series applied, in the build's order,
# to the files it touches at a RetroArch ref (M6 T3, #650; brief section 4
# Q4 (c), #650 criterion 9).
#
#   q4c-patches.sh <patches-dir> <ref> <outdir>
#
# Fetches every file the series touches at <ref> from libretro/RetroArch
# through `gh api` (raw media type; no clone, no build), into
# <outdir>/src. Then, in scripts/unpack's order (patches/*.patch sorted, then
# patches/batteryplus/), for each patch:
#   git apply --check -p1    (the criterion's form)
#   patch -p1 --fuzz=0 --dry-run
# and then `patch -p1` as scripts/unpack runs it (default fuzz), so the next
# patch meets the tree the build would give it. One line per patch:
#   <patch> git-apply=<ok|FAIL> fuzz0=<ok|FAIL> applied=<clean|offset|fuzz|FAILED>
# Run it at the pin first: the series must apply there, or this method is
# wrong (the control).
set -u
P=$1 REF=$2 OUT=$3
rm -rf "$OUT"; mkdir -p "$OUT/src"
files=$(grep -h -E '^\+\+\+ ' "$P"/*.patch "$P"/batteryplus/*.patch | sed -E 's#^\+\+\+ ##; s#\t.*##; s# .*##; s#^[^/]+/##' | sort -u)
for f in $files; do
  mkdir -p "$OUT/src/$(dirname "$f")"
  if ! GH_PAGER= gh api -H "Accept: application/vnd.github.raw" "repos/libretro/RetroArch/contents/$f?ref=$REF" > "$OUT/src/$f" 2> "$OUT/fetch.err"; then
    echo "fetch FAILED $f: $(tail -1 "$OUT/fetch.err")"; rm -f "$OUT/src/$f"
  fi
done
echo "fetched $(find "$OUT/src" -type f | wc -l) of $(echo "$files" | wc -w) files at $REF"
cd "$OUT/src" || exit 2
for p in $(ls "$P"/*.patch | sort) $(ls "$P"/batteryplus/*.patch); do
  n=${p#"$P"/}
  ga=$(git apply --check -p1 "$p" >/dev/null 2>&1 && echo ok || echo FAIL)
  f0=$(patch -p1 --fuzz=0 --dry-run -s < "$p" >/dev/null 2>&1 && echo ok || echo FAIL)
  log=$(patch -p1 --no-backup-if-mismatch < "$p" 2>&1); rc=$?
  if [ $rc -ne 0 ]; then a=FAILED; elif echo "$log" | grep -q 'with fuzz'; then a=fuzz; elif echo "$log" | grep -q 'offset'; then a=offset; else a=clean; fi
  echo "$n git-apply=$ga fuzz0=$f0 applied=$a"
  [ $rc -ne 0 ] && echo "$log" | grep -E 'FAILED|saving rejects|No file' | sed 's/^/    /'
done
