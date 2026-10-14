#!/bin/bash
# Run only inside the coordinator's allocated, disposable installed-image VM.
# Foreground exec leaves process ownership, original exits and timeout to its owner.
set -euo pipefail
case "${1:-}" in
  gc|gc-qt)
    rom=/storage/roms/gamecube/SuDokuL-GC.dol
    digest=e5995f4dc27d5fbd4d5e4eb0c1b8161fca5c730d9f294e2eba9c942658e2474d
    system=gamecube; emulator=dolphin; core=dolphin-sa-gc
    [[ $1 != gc-qt ]] || core=dolphin-qt-gc ;;
  wii|wii-qt)
    rom=/storage/roms/wii/SuDokuL-Wii.dol
    digest=e4fc81977b527538d7fa8d6427099c21c0f2502d18b81a58134f8f07416a8455
    system=wii; emulator=dolphin; core=dolphin-sa-wii
    [[ $1 != wii-qt ]] || core=dolphin-qt-wii ;;
  flycast-game)
    rom=/storage/roms/dreamcast/demon-bazooka.cdi
    digest=c3065546fba82020a9692432b99b45e3bffe661a3b6c2fb2cc73fafc82e332f3
    system=dreamcast; emulator=flycast; core=flycast-sa ;;
  flycast-vmu-diagnostic)
    rom=/storage/roms/dreamcast/dreamcast-basic.cdi
    digest=5c359e19cc76c6ecdf89ab509c7d80e727943a7181330ad22fd98d4a8695651d
    system=dreamcast; emulator=flycast; core=flycast-sa ;;
  *) echo 'usage: native-launch.sh gc|gc-qt|wii|wii-qt|flycast-game|flycast-vmu-diagnostic' >&2; exit 2 ;;
esac
printf '%s  %s\n' "$digest" "$rom" | sha256sum --check --status
exec /usr/bin/runemu.sh "$rom" "-P$system" "--core=$core" \
  "--emulator=$emulator" "--controllers=${CONTROLLERSCONFIG:-}"
