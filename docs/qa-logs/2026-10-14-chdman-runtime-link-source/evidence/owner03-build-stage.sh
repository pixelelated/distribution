#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# UNRUN. One stage per coordinator-watched offline allocation; no default stage.
# Source export, admission, timeouts/process-group cleanup, receipts and binary
# qualification belong to the external coordinator runner, not this entrypoint.
set -euo pipefail
[[ $# == 1 ]] || { echo 'Supply exactly one documented build stage' >&2; exit 64; }
: "${PIX574_OWNER:?fresh coordinator-owned absolute scratch directory required}"
: "${PIX574_TC:?retained toolchain at its original container prefix required}"
[[ $PIX574_OWNER == /* && $PIX574_OWNER != / && $PIX574_OWNER != *' '* ]] || exit 64
[[ $(realpath -- "$PIX574_OWNER") == "$PIX574_OWNER" ]] || exit 64
[[ -d $PIX574_OWNER/tmp ]] || exit 64
packet=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
export TMPDIR="$PIX574_OWNER/tmp"
export CCACHE_DISABLE=1
export CCACHE_DIR="$PIX574_OWNER/tmp/ccache"
export PATH="$PIX574_TC/bin:/usr/bin:/bin"
export PKG_CONFIG_SYSROOT_DIR="$PIX574_TC/x86_64-rocknix-linux-gnu/sysroot"
export PKG_CONFIG_LIBDIR="$PKG_CONFIG_SYSROOT_DIR/usr/lib/pkgconfig:$PKG_CONFIG_SYSROOT_DIR/usr/share/pkgconfig"
unset PKG_CONFIG_PATH ARCH PROJECT DISTRO MAKEFLAGS MFLAGS CC CXX CPP LD AR
unset CFLAGS CXXFLAGS CPPFLAGS LDFLAGS ASFLAGS
cmake="$PIX574_TC/bin/cmake"
make="$PIX574_TC/bin/make"
cc="$PIX574_TC/bin/x86_64-rocknix-linux-gnu-gcc"
cxx="$PIX574_TC/bin/x86_64-rocknix-linux-gnu-g++"
ar="$PIX574_TC/bin/x86_64-rocknix-linux-gnu-ar"
dolphin="$PIX574_OWNER/dolphin-src"
mame="$PIX574_OWNER/mame-24cffe763621b164fc10be2ae3660f140be25182"
# Source roots must be real private directories, not links back into custody.
case "$1" in
  dolphin-*) [[ -d $dolphin && $(realpath -- "$dolphin") == "$dolphin" ]] || exit 64 ;;
  chdman-*) [[ -d $mame && $(realpath -- "$mame") == "$mame" ]] || exit 64 ;;
  *) echo 'Unknown stage' >&2; exit 64 ;;
esac
case "$1" in
  dolphin-configure)
    [[ ! -e $PIX574_OWNER/dolphin-build ]] || exit 64
    exec "$cmake" -S "$dolphin" -B "$PIX574_OWNER/dolphin-build" -G Ninja \
      -C "$packet/dolphin-options.cmake" \
      -DCMAKE_TOOLCHAIN_FILE="$PIX574_TC/etc/cmake-x86_64-rocknix-linux-gnu.conf" \
      -DCMAKE_SYSROOT="$PKG_CONFIG_SYSROOT_DIR" \
      -DPKG_CONFIG_EXECUTABLE="$PIX574_TC/bin/pkg-config" \
      -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_FLAGS_RELEASE='-O1 -DNDEBUG' \
      -DCMAKE_CXX_FLAGS_RELEASE='-O1 -DNDEBUG' -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
    ;;
  dolphin-build)
    exec "$cmake" --build "$PIX574_OWNER/dolphin-build" --parallel 1 --target dolphin-tool
    ;;
  chdman-bootstrap)
    # Native GENie only. Never build it with the target overrides or target flags.
    exec "$make" -C "$mame/3rdparty/genie/build/gmake.linux" -f genie.make -j1 \
      config=release verbose=1 CC=/usr/bin/gcc CXX=/usr/bin/g++ AR=/usr/bin/ar
    ;;
  chdman-configure)
    [[ ! -e $mame/build/projects/sdl/mame/gmake-linux/Makefile ]] || exit 64
    # Require the exact documented scratch-only adjustment; never patch custody.
    [[ $(sha256sum "$mame/scripts/genie.lua" | cut -d ' ' -f 1) == 60be68969448508ba3a130f64044ec196f6d52970337889474c85bcb075c40ba ]] || exit 64
    # Require the separate exact scratch-only OSD selection correction.
    [[ $(sha256sum "$mame/scripts/toolchain.lua" | cut -d ' ' -f 1) == b45c6d1fa1d4d4a824d1f739ab749d2ae776dfb23b7a040b89bc4d2c67c2219b ]] || exit 64
    # Explicit version/project targets avoid the broad 'generate' target's
    # translations/layout generation and avoid building all tools/emulators.
    exec "$make" -C "$mame" -j1 \
      build/generated/version.cpp build/projects/sdl/mame/gmake-linux/Makefile \
      TARGET=mame SUBTARGET=mame OSD=sdl TARGETOS=linux CROSS_BUILD=1 PTR64=1 \
      TOOLS=1 EMULATOR=0 TESTS=0 BENCHMARKS=0 \
      IGNORE_GIT=1 NEW_GIT_VERSION=24cffe763621b164fc10be2ae3660f140be25182 \
      PYTHON_EXECUTABLE=python3 VERBOSE=1 NOWERROR=1 PRECOMPILE=0 \
      OPTIMIZE=1 SYMBOLS=0 STRIP_SYMBOLS=0 LTO=0 OPENMP=0 \
      NO_OPENGL=1 NO_X11=1 NO_USE_XINPUT=1 NO_USE_XINPUT_WII_LIGHTGUN_HACK=1 \
      NO_USE_MIDI=1 NO_USE_PORTAUDIO=1 NO_USE_PULSEAUDIO=1 NO_USE_PIPEWIRE=1 \
      USE_QTDEBUG=0 USE_TAPTUN=0 USE_PCAP=0 \
      USE_SYSTEM_LIB_ZLIB=0 USE_SYSTEM_LIB_ZSTD=0 USE_SYSTEM_LIB_FLAC=0 \
      USE_SYSTEM_LIB_EXPAT=0 USE_SYSTEM_LIB_UTF8PROC=0 \
      CC=/usr/bin/gcc CXX=/usr/bin/g++ \
      OVERRIDE_CC="$cc" OVERRIDE_CXX="$cxx" OVERRIDE_LD="$cxx" OVERRIDE_AR="$ar"
    ;;
  chdman-build)
    exec "$make" -C "$mame/build/projects/sdl/mame/gmake-linux" -j1 \
      config=release64 verbose=1 chdman
    ;;
  *) echo 'Unknown stage' >&2; exit 64 ;;
esac
