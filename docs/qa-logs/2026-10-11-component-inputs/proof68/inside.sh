#!/bin/bash
set -e
export PROJECT=ROCKNIX DEVICE=GENERIC_X64 ARCH=x86_64
export BUILD_DIR=/proof/build SOURCES_DIR=/proof/sources
python3 --version
./scripts/unpack idtech-lr
set +e
. config/options idtech-lr
set -e
printf '%s  %s\n' "$PKG_SHA256" "$PKG_BUILD/doom.tar.gz" | sha256sum -c -
mkdir -p /proof/no-network
printf '#!/bin/sh\nexit 97\n' > /proof/no-network/curl
cp /proof/no-network/curl /proof/no-network/wget
chmod +x /proof/no-network/*
export PATH=/proof/no-network:$PATH
INSTALL=/proof/installed
makeinstall_target
cmp "$PKG_BUILD/doom.tar.gz" "$INSTALL/usr/share/idtech/doom.tar.gz"
printf 'PASS real unpack and offline installation preserve archive bytes\n'
set +e
. config/options harfbuzz-icu
set -e
printf 'EFFECTIVE harfbuzz-icu PKG_LICENSE=%s PKG_VERSION=%s\n' "$PKG_LICENSE" "$PKG_VERSION"
# Exercise the actual framework downloader with a corrupt downloaded body.
mkdir -p /proof/corrupt-bin
cat > /proof/corrupt-bin/wget <<'BAD'
#!/bin/bash
while [ "$#" -gt 0 ]; do
 if [ "$1" = -O ]; then shift; printf 'corrupt QA fixture\n' > "$1"; exit 0; fi
 shift
done
exit 97
BAD
chmod +x /proof/corrupt-bin/wget
export PATH=/proof/corrupt-bin:$PATH SOURCES_DIR=/proof/corrupt-sources
if ./scripts/get idtech-lr > /proof/corrupt-download.log 2>&1; then
 echo 'FAIL corrupted download was accepted'; exit 1
fi
! test -f /proof/corrupt-sources/idtech-lr/idtech-lr-doom-1.0.tar.gz.sha256
printf 'PASS real downloader refuses corrupt body and leaves no acceptance stamp\n'
