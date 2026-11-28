#!/bin/bash
# #1477 on build 26 (round 6169621a4b, ES e67f28e18): the end-of-game wait,
# EN and FR at 640x480 (D-CLOUD-198, D-RA-057).
#  A  a saves sync during the wait: time-to-play's g2g-midsync cell (its
#     stall endpoint holds the sync to the 15 s bound);
#  B  a startup sync still moving bytes at 15 s: the QA WebDAV throttled to
#     20 KiB/s, a 1 MiB save beside the probe ROM, a launch as the sync runs;
#  C  the achievements' send in the wait: one synthetic held award, the proxy
#     pointed at a loopback stand-in that holds the award request 6 s then
#     accepts it; EmulationStation and the proxy restarted together (the
#     startup sync, and the proxy's flush at its start), a launch as the sync
#     runs: the page should name the saves, then the send, then start the game.
# QA guest only; no real account. Step rc files in $C.
C=/workspace/tmp/rocknix-session/p1477-b26; mkdir -p $C
F=/workspace/tmp/rocknix-session/1477-fixture
ROUND=/workspace/repos/rocknix.worktrees/m7-rc-round-20261125; KEY=/tmp/rocknix-vm-pair/qa-key; MON=/tmp/rocknix-qemu-monitor.sock
IMG=$(ls /workspace/repos/rocknix.worktrees/m7-round-x64-20261125/target/pixelelated-GENERIC_X64.x86_64-*.g6169621a4b*-from-ROCKNIX.img.gz | head -1)
SSHO=(-F /dev/null -p 10022 -i $KEY -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=10)
SCPO=(-F /dev/null -P 10022 -i $KEY -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=10)
S() { timeout 180 ssh -n "${SSHO[@]}" root@127.0.0.1 ". /etc/profile >/dev/null 2>&1; $*"; }
mask() { sed -E 's/((token|key|passw[a-z]*|psk|user)[=:])[^ ]*/\1***/Ig'; }
BK=$ROUND/tools/cloud-test-backend
reboot_guest() {
    local b0 b i; b0=$(S 'cat /proc/sys/kernel/random/boot_id')
    S 'sync; systemctl reboot' >/dev/null 2>&1
    for i in $(seq 1 60); do sleep 3; b=$(S 'cat /proc/sys/kernel/random/boot_id' 2>/dev/null); [ -n "$b" ] && [ "$b" != "$b0" ] && return 0; done; return 1
}
launch_when_syncing() {  # $1 the ROM; waits for ES's API and rclone, then POSTs the launch
    local i
    for i in $(seq 1 120); do S 'curl -s -m 2 http://127.0.0.1:1234/isIdle' >/dev/null 2>&1 && break; sleep 0.5; done
    for i in $(seq 1 120); do S 'pgrep -f "rclon[e] " >/dev/null' && break; sleep 0.5; done
    echo "launch sent $(date -u +%T.%N | cut -c1-12) UTC http $(S "curl -s -o /dev/null -w '%{http_code}' -X POST -H 'Content-Type: text/plain' --data $1 http://127.0.0.1:1234/launch")"
}
burst() {  # $1 outdir $2 frames
    mkdir -p "$1"; { for i in $(seq -w 1 $2); do echo "shot burst-$i"; echo "wait 1"; done; } > "$1.steps"
    timeout 300 $ROUND/tools/vm-visual-qa --monitor $MON run "$1.steps" --outdir "$1" > "$1.log" 2>&1
}
[ -n "$IMG" ] || { echo 2 > $C/rc; exit 2; }
(cd $ROUND && VM_RES=640x480 timeout 900 tools/vm-pair up "$IMG") > $C/up.log 2>&1 || { echo 2 > $C/rc; exit 2; }
"$BK" seed-device > $C/seed.sh && scp -q "${SCPO[@]}" $C/seed.sh root@127.0.0.1:/tmp/seed.sh < /dev/null && S 'bash /tmp/seed.sh >/dev/null 2>&1; rm -f /tmp/seed.sh; mkdir -p /storage/roms/gb /storage/m7-qa-1477'
scp -q "${SCPO[@]}" $F/TTProbe.gb $F/award-standin.py $F/award-seed.py root@127.0.0.1:/storage/m7-qa-1477/ < /dev/null && S 'cp /storage/m7-qa-1477/TTProbe.gb /storage/roms/gb/TTProbe.gb'
S 'sed -n "s/^BUILD_ID=//p" /etc/os-release' > $C/build-id.txt

# A
for lang in en fr; do
    code=en_US; [ $lang = fr ] && code=fr_FR
    S "set_setting system.language $code"; reboot_guest; sleep 30
    (cd $ROUND && timeout 1200 tools/time-to-play --port 10022 --identity $KEY --monitor $MON --backend webdav \
        --out $C/A-$lang --only g2g-midsync --repeat 1 --vm --label "#1477 case A $lang, build 26") > $C/A-$lang.log 2>&1
    echo $? > $C/A-$lang.rc
done

# B
for lang in en fr; do
    code=en_US; [ $lang = fr ] && code=fr_FR
    "$BK" down > $C/B-$lang-backend.log 2>&1; CLOUD_QA_BWLIMIT=20k "$BK" up >> $C/B-$lang-backend.log 2>&1
    S "set_setting system.language $code; set_setting cloudsaves.startup 1; sed -i 's/^video_driver = .*/video_driver = \"gl\"/' /storage/.config/retroarch/retroarch.cfg; dd if=/dev/urandom of=/storage/roms/gb/TTProbe.srm bs=1024 count=1024 2>/dev/null; rm -f /storage/.cache/cloud_sync/last-sync-startup" > $C/B-$lang.arm.log 2>&1
    reboot_guest
    launch_when_syncing /storage/roms/gb/TTProbe.gb > $C/B-$lang.launch.txt
    burst $C/B-$lang 40
    S 'echo "last-sync-startup: $(cat /storage/.cache/cloud_sync/last-sync-startup 2>&1)"; echo "retroarch: $(pidof retroarch)"' >> $C/B-$lang.launch.txt 2>&1
    S 'killall -TERM retroarch 2>/dev/null; sleep 5; rm -f /storage/roms/gb/TTProbe.srm; set_setting cloudsaves.startup 0'
    echo 0 > $C/B-$lang.rc
done
"$BK" down >> $C/backend-restore.log 2>&1; "$BK" up >> $C/backend-restore.log 2>&1

# C
for lang in en fr; do
    code=en_US; [ $lang = fr ] && code=fr_FR
    S "set_setting system.language $code; set_setting cloudsaves.startup 1; set_setting global.retroachievements 0; sed -i 's/^video_driver = .*/video_driver = \"gl\"/' /storage/.config/retroarch/retroarch.cfg; [ \"\$(get_setting global.retroachievements.offlineproxy)\" = 1 ] || raofflineproxy-ctl enable >/dev/null 2>&1; echo toggle=\$(get_setting global.retroachievements.offlineproxy)" > $C/C-$lang.arm.log 2>&1
    reboot_guest; sleep 20
    S "systemctl stop essway; systemctl stop raofflineproxy; mkdir -p /storage/.config/raofflineproxy; python3 - <<'PY'
import json
from pathlib import Path
p = Path('/storage/.config/raofflineproxy/config.json'); d = json.loads(p.read_text()) if p.exists() and p.read_text().strip() else {}
d['upstream_host'] = 'http://127.0.0.1:18602'; p.write_text(json.dumps(d, indent=2) + '\n')
PY
python3 /storage/m7-qa-1477/award-seed.py; systemctl stop ra-award-1477 2>/dev/null; systemd-run --unit=ra-award-1477 --quiet python3 /storage/m7-qa-1477/award-standin.py 18602 6; sleep 1; rm -f /storage/.cache/cloud_sync/last-sync-startup; systemctl reset-failed raofflineproxy 2>/dev/null; systemctl start raofflineproxy; systemctl start essway; echo pending=\$(raofflineproxy-ctl pending 2>&1 | tail -1)" >> $C/C-$lang.arm.log 2>&1
    launch_when_syncing /storage/roms/gb/TTProbe.gb > $C/C-$lang.launch.txt
    burst $C/C-$lang 30
    S 'echo "last-sync-startup: $(cat /storage/.cache/cloud_sync/last-sync-startup 2>&1)"; echo "pending now: $(raofflineproxy-ctl pending 2>&1 | tail -1)"; echo "retroarch: $(pidof retroarch)"; journalctl -u ra-award-1477 --no-pager | grep standin | tail -2' 2>&1 | mask >> $C/C-$lang.launch.txt
    S 'killall -TERM retroarch 2>/dev/null; sleep 5; systemctl stop ra-award-1477 2>/dev/null; rm -f /storage/.config/raofflineproxy/config.json; set_setting cloudsaves.startup 0'
    echo 0 > $C/C-$lang.rc
done
S "set_setting system.language en_US"
(cd $ROUND && tools/vm-pair down) >> $C/up.log 2>&1; rm -f /tmp/rocknix-vm-pair/vm-*.qcow2 /tmp/rocknix-vm-pair/vm-*.ovmf-vars.fd
echo 0 > $C/rc
