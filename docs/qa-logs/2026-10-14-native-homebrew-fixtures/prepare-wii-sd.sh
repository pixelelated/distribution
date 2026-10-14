#!/bin/bash
# Future allocated preparation only. Creates a new 128 MiB FAT SD image; no mount.
set -euo pipefail
[[ $# == 1 ]] || { echo 'usage: prepare-wii-sd.sh NEW_SD_IMAGE' >&2; exit 2; }
image=$1
[[ ! -e $image && ! -L $image ]] || { echo 'refusing existing SD image' >&2; exit 2; }
command -v mformat >/dev/null
command -v mmd >/dev/null
mformat -C -i "$image" -T 262144 -v PIXM7QA ::
[[ $(stat -c %s "$image") == 134217728 ]]
mmd -i "$image" ::/apps
mmd -i "$image" ::/apps/SuDokuL
mdir -i "$image" ::/apps/SuDokuL
sha256sum "$image"
