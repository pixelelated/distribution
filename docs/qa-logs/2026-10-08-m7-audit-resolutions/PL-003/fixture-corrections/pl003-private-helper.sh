set -e
cat /proc/self/mountinfo > /storage/qa524/mountinfo-before-private.txt
mount --make-rprivate /
for target in /usr/bin/cloud_setup /storage/qa524/frozen/usr/bin/cloud_setup; do
 n=0
 while awk -v target="$target" '$5==target{found=1} END{exit !found}' /proc/self/mountinfo; do
  n=$((n+1)); test "$n" -lt 128
  umount "$target"
 done
done
mkdir -p /storage/qa524/delegate
cp /storage/qa524/clean-cloud-setup /storage/qa524/delegate/cloud_setup
chmod 755 /storage/qa524/delegate/cloud_setup
cp /storage/qa524/delegate/cloud_setup /usr/bin/cloud_setup.qa524
mv /usr/bin/cloud_setup.qa524 /usr/bin/cloud_setup
sha256sum /usr/bin/cloud_setup /storage/qa524/delegate/cloud_setup /storage/qa524/frozen/usr/bin/cloud_setup
cat /proc/self/mountinfo > /storage/qa524/mountinfo-after-private.txt
cat /proc/sys/kernel/random/boot_id
journalctl --list-boots
