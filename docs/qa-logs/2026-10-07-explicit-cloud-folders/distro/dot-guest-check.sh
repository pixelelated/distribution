#!/bin/bash
set -eu
O=/storage/qa-508/dot-proof
mkdir -p "$O"
cp -p /storage/.config/cloud_sync.conf "$O/original.conf"
trap 'cp -p "$O/original.conf" /storage/.config/cloud_sync.conf; rm -f "$O/original.conf"' EXIT
for tier in SAVES_REMOTE SETTINGS_REMOTE CONTENT_REMOTE; do
  cp -p "$O/original.conf" /storage/.config/cloud_sync.conf
  sed -i "s|^${tier}=.*|${tier}=\"./\"|" /storage/.config/cloud_sync.conf
  before=$(sha256sum /storage/.config/cloud_sync.conf)
  for mode in --folder-state --seed-folders; do
    rc=0
    /usr/bin/cloud_setup "$mode" > "$O/$tier-${mode#--}.log" 2>&1 || rc=$?
    [ "$rc" -ne 0 ]
    grep -q "^>>> why YOUR CLOUD SYNC SETTINGS COULDN'T BE READ" "$O/$tier-${mode#--}.log"
    [ "$before" = "$(sha256sum /storage/.config/cloud_sync.conf)" ]
    printf 'VERIFIED %s %s refused rc=%s; configured values unchanged\n' "$tier" "$mode" "$rc"
  done
done
sha256sum /usr/bin/cloud_setup
