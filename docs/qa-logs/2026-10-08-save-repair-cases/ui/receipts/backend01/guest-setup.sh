set -eu
ip route replace blackhole 0.0.0.0/1
ip route replace blackhole 128.0.0.0/1
ip -6 route replace blackhole ::/1
ip -6 route replace blackhole 8000::/1
ip route
ip -6 route
cd /storage/qa520
tar xf payload.tar
cp -a frozen/usr/bin/. /usr/bin/
for f in frozen/usr/config/*; do
  name=${f##*/}
  mount --bind "$PWD/$f" "/usr/config/$name"
  cp "$f" "/storage/.config/$name"
done
cp -a frozen/provider/. provider/
cat > /storage/.config/rclone/rclone.conf <<'CONF'
[qa]
type = webdav
url = http://127.0.0.1:9038
vendor = other
CONF
chmod 600 /storage/.config/rclone/rclone.conf
nohup rclone serve webdav /storage/qa520/provider --addr 127.0.0.1:9038 --log-file /storage/qa520/provider.log >/storage/qa520/provider.stdout 2>&1 </dev/null &
echo $! > /storage/qa520/provider.pid
sleep 1
kill -0 "$(cat /storage/qa520/provider.pid)"
cloud_setup --set-saves-remote /QA-PSP/Saves
cloud_setup --set-settings-remote /QA-PSP/Backups
cloud_setup --set-content-remote /QA-PSP/Content
cloud_setup --validation-context
find /storage/qa520/provider -type f -exec sha256sum '{}' ';' | sort
