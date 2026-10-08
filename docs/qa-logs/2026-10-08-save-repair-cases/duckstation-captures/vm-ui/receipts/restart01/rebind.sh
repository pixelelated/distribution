set -eu
ip route replace blackhole 0.0.0.0/1
ip route replace blackhole 128.0.0.0/1
ip -6 route replace blackhole ::/1
ip -6 route replace blackhole 8000::/1
systemctl stop essway.service
mount -t overlay overlay -o lowerdir=/usr/bin,upperdir=/storage/qa520/upper,workdir=/storage/qa520/work /usr/bin
mount --bind /storage/qa520/emulationstation /usr/bin/emulationstation
mount --bind /storage/qa520/fr.mo /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo
for f in /storage/qa520/frozen/usr/config/*; do name=${f##*/}; mount --bind "$f" "/usr/config/$name"; done
mount --bind /storage/qa521/duckstation-sa /usr/bin/duckstation-sa
mount --bind /storage/qa521/frozen/settings.ini /usr/config/duckstation/settings.ini
chmod 755 '/storage/qa521/frozen/Start Duckstation.sh'
mount --bind '/storage/qa521/frozen/Start Duckstation.sh' '/usr/config/modules/Start Duckstation.sh'
nohup rclone serve webdav /storage/qa520/provider --addr 127.0.0.1:9038 --dir-cache-time 0 --log-file /storage/qa520/provider.log >/storage/qa520/provider.stdout 2>&1 </dev/null &
echo $! > /storage/qa520/provider.pid
sleep 1
kill -0 "$(cat /storage/qa520/provider.pid)"
sha256sum /usr/bin/emulationstation /usr/share/locale/fr/LC_MESSAGES/emulationstation2.mo /usr/bin/duckstation-sa /usr/bin/duckstation_screenshot_path /usr/bin/start_duckstation.sh /usr/config/duckstation/settings.ini '/usr/config/modules/Start Duckstation.sh'
ip route
ip -6 route
stat -c '%a %n' /usr/bin/duckstation-sa /usr/bin/duckstation_screenshot_path '/usr/config/modules/Start Duckstation.sh'
