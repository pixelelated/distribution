set -eu
mkdir -p /storage/qa521/libupper /storage/qa521/libwork
mount -t overlay overlay -o lowerdir=/usr/lib,upperdir=/storage/qa521/libupper,workdir=/storage/qa521/libwork /usr/lib
for n in libcom_err.so libcom_err.so.2 libcom_err.so.2.1; do install -m 0755 /storage/qa521/libcom_err.so.2.1 /usr/lib/$n; done
sha256sum /usr/lib/libcom_err.so*
. /etc/profile
timeout 20 /usr/bin/duckstation-sa -help
