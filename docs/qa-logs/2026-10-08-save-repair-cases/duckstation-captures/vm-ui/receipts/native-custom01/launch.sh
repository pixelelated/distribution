. /etc/profile
cd /storage
nohup setsid /usr/bin/duckstation-sa -nogui -fullscreen -bios > /storage/qa521/native-custom.log 2>&1 </dev/null &
echo $! > /storage/qa521/native.pid
sleep 8
kill -0 "$(cat /storage/qa521/native.pid)"
tail -n 35 /storage/qa521/native-custom.log
