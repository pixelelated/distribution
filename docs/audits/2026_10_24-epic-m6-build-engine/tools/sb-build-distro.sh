#!/usr/bin/env bash
# E5 (#652, #833; PL-20, PL-24): three blocks of scripts/build_distro, and
# scripts/image's identity refusal, lifted by their own marker lines from a
# commit (or the working tree) and run over a fixture directory in the scratch
# directory given. The real build_distro is not run: it would enter
# tools/watch-build, and its nesting marker is never pre-set (device-builds.md).
#   sb-build-distro.sh <scratch-dir> [commit|WORKTREE]
# Case 1 (#833): BUILD_TIMESTAMP frozen, target/ holding an output of that
#   identity and an older one; the prune then the image's refusal.
# Case 2 (PL-20): `make image` failing under set -e.
# Case 3 (PL-24): the clean block for a device without DEVICE_ROOT, one clean failing.
set -uo pipefail
S="${1:?scratch directory}"; R="${2:-8ebaf8daad}"
REPO="$(git rev-parse --show-toplevel)"
W="$S/run-$(date +%s%N)"; mkdir -p "$W/config" "$W/scripts" "$W/target" "$W/bin"
src() { if [ "$R" = WORKTREE ]; then cat "$REPO/$1"; else git -C "$REPO" show "$R:$1"; fi; }
src config/build-identity > "$W/config/build-identity"
src scripts/build_distro > "$W/build_distro.src"; src scripts/image > "$W/image.src"
# blocks, by marker
awk '/^# Prune old releases/{on=1} /^# Remove image root/{on=0} on' "$W/build_distro.src" > "$W/prune.sh"
awk '/^# One identity for the installed system/{on=1} on{print} on && /Build identity already exists/{getline; print; exit}' "$W/image.src" > "$W/identity.sh"
awk '/^case "\$\{ARCH\}" in/{on=1} on' "$W/build_distro.src" > "$W/tail.sh"
awk '/^if \[ -z "\$\{DIRTY\}" \]; then/{on=1} on{print} on && /^fi$/{exit}' "$W/build_distro.src" > "$W/clean.sh"
cd "$W"
export GIT_CONFIG_GLOBAL=/dev/null GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@invalid
git init -q . && printf 'target/\nrelease/\nbuild.*/\nbin/\n*.sh\n*.src\nout-*\n' > .gitignore && git add .gitignore config && git commit -q -m fixture-1
H=$(git rev-parse HEAD)
STUBS='die() { echo "die: $*" >&2; exit 1; }; show_config() { :; }'
common=(PATH="$W/bin:/usr/bin:/bin" HOME="$W" DISTRONAME=pixelelated DEVICE=H700 ARCH=aarch64 TARGET_ARCH=aarch64 PROJECT=ROCKNIX)

echo "## case 1: a frozen BUILD_TIMESTAMP whose identity is already in target/"
TS=20261024T000000Z
name="pixelelated-H700.aarch64-0.0.1-dev+${TS}.g${H:0:12}"
echo fixture-2 > "target/${name}.img.gz"; echo fixture-3 > "target/${name}.identity.json"
echo fixture-4 > "target/pixelelated-H700.aarch64-0.0.1-dev+20261023T000000Z.g${H:0:12}.img.gz"
before=$(cd target && sha256sum "${name}".* | sha256sum | cut -c1-16)
env -i "${common[@]}" ROOT="$W" TARGET_IMG="$W/target" BUILD="$W/build.pixelelated-H700.aarch64" OS_VERSION=0.0.1 BUILD_TIMESTAMP="$TS" \
  bash -c "set -e; $STUBS; mkdir -p \"\$BUILD\"; . ./prune.sh; . ./identity.sh; echo 'image step: would assemble' \"\$IMAGE_NAME\"" > out-1 2>&1
echo "exit: $?"; grep -E '^(die:|image step:|Prune)' out-1 | sed "s#$W#<fixture>#g"
after=$(cd target && sha256sum "${name}".* 2>/dev/null | sha256sum | cut -c1-16)
echo "the identity's files: $([ "$before" = "$after" ] && echo byte-identical || echo REMOVED OR CHANGED)"
echo "target now: $(ls target | tr '\n' ' ')"

echo "## case 2: make image fails"
printf '#!/bin/sh\nexit 2\n' > bin/make; chmod +x bin/make
env -i "${common[@]}" bash -c "set -e; $STUBS; . ./tail.sh; echo 'after the case: reached'" > out-2 2>&1
echo "exit: $?"; sed 's/^/  /' out-2 | head -3

echo "## case 3: the clean block, DEVICE=H700, no DEVICE_ROOT, one clean failing"
mkdir -p build.pixelelated-H700.aarch64/.stamps/initramfs build.pixelelated-H700.aarch64/initramfs
echo fixture-5 > build.pixelelated-H700.aarch64/.stamps/initramfs/build_init
printf '#!/bin/sh\n[ "$1" = fixture-fails ] && exit 1\nexit 0\n' > scripts/clean; chmod +x scripts/clean
env -i "${common[@]}" PKG_CLEAN="fixture-ok fixture-fails" bash -c "set -e; $STUBS; . ./clean.sh" > out-3 2>&1
echo "exit: $?"; grep -v '^Clean: fixture-ok$' out-3 | sed 's/^/  /'
echo "initramfs stamp: $([ -e build.pixelelated-H700.aarch64/.stamps/initramfs ] && echo 'still there' || echo removed)"
