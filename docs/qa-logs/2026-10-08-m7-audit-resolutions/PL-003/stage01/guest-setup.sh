set -eu
ip route replace blackhole 0.0.0.0/1
ip route replace blackhole 128.0.0.0/1
ip -6 route replace blackhole ::/1
ip -6 route replace blackhole 8000::/1
cd /storage/qa524
tar xf payload.tar
cp -a frozen/usr/bin/. /usr/bin/
for f in frozen/usr/config/*; do
 name=${f##*/}
 mount --bind "$PWD/$f" "/usr/config/$name"
 cp "$f" "/storage/.config/$name"
done
cat > /storage/.config/rclone/rclone.conf <<'CONF'
[qa]
type = webdav
url = http://127.0.0.1:9038
vendor = other
CONF
chmod 600 /storage/.config/rclone/rclone.conf
mkdir -p provider/QA/Saves provider/QA/Backups provider/QA/Content local-witness
printf 'synthetic saved bytes 524\n' > provider/QA/Saves/witness.srm
printf 'synthetic backup bytes 524\n' > provider/QA/Backups/witness.txt
printf 'synthetic content bytes 524\n' > provider/QA/Content/witness.txt
printf 'synthetic local bytes 524\n' > local-witness/witness.srm
nohup rclone serve webdav /storage/qa524/provider --addr 127.0.0.1:9038 --dir-cache-time 0 --log-file /storage/qa524/provider.log >/storage/qa524/provider.stdout 2>&1 </dev/null &
echo $! > /storage/qa524/provider.pid
sleep 1
kill -0 "$(cat provider.pid)"
cloud_setup --set-saves-remote /QA/Saves
cloud_setup --set-settings-remote /QA/Backups
cloud_setup --set-content-remote /QA/Content
cloud_setup --validation-context
sha256sum /storage/.config/cloud_sync.conf /storage/.config/rclone/rclone.conf
find /storage/qa524/provider /storage/qa524/local-witness -type f -exec sha256sum '{}' ';' | sort
