set -eu
systemctl stop essway.service
nohup python3 /storage/qa521/virtualpad.py > /storage/qa521/pad.log 2>&1 </dev/null &
sleep 1
kill -0 "$(cat /storage/qa521/pad.pid)"
cat /proc/bus/input/devices
. /etc/profile
cd /storage
nohup setsid /usr/bin/duckstation-sa -nogui -fullscreen -bios > /storage/qa521/native-default.log 2>&1 </dev/null &
echo $! > /storage/qa521/native.pid
sleep 8
kill -0 "$(cat /storage/qa521/native.pid)"
ps | grep -E 'duckstation|virtualpad' | grep -v grep
cat /storage/qa521/native.pid
tail -n 80 /storage/qa521/native-default.log
