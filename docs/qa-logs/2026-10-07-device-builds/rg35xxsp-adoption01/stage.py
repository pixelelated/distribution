#!/usr/bin/env python3
"""Issue #500: exact authorized H700 transfer via a loopback-only SSH tunnel."""
from pathlib import Path
import datetime, hashlib, http.server, json, os, re, shutil, subprocess, threading, time
OWNER = Path('/workspace/tmp/pixelelated-m7-rg35xxsp-adoption-01')
TREE = Path('/workspace/repos/rocknix.worktrees/conflict-resolution')
BUNDLE = Path('/workspace/artifacts/pixelelated-candidates/sha256/d89b067a5176d7c02633bc9e72ee9b0f96dd3d626d343a0f16949e70c9daf710')
NAME = 'pixelelated-H700.aarch64-0.0.1-from-ROCKNIX.tar'
SHA = 'a419dc33e1f3be2c422cac4b89d85cf104f363c3da6ed7059e0a8aa531bfd014'
ARTIFACT = BUNDLE / NAME
REMOTE = '/storage/.cache/' + NAME + '.m7-500.part'
QUEUE = '/storage/.update/' + NAME
SSH = ['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=8', 'rg35xxsp']
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def record(name, value):
    with (OWNER / name).open('x') as f: json.dump(value, f, indent=2); f.write('\n')
def filtered(data): return '\n'.join(s for s in data.splitlines() if not re.search('key|pass|token|user|psk',s,re.I))+'\n'
def readback(name, command):
    r=subprocess.run(SSH+[command],capture_output=True,text=True,timeout=40)
    (OWNER/name).write_text(filtered(r.stdout+r.stderr))
    if r.returncode: raise RuntimeError('readback failed: '+name)
    return r.stdout
class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def do_GET(self):
        if self.path != '/firmware.tar': self.send_error(404); return
        self.send_response(200);self.send_header('Content-Length',str(ARTIFACT.stat().st_size));self.end_headers()
        total=0;last=time.monotonic()
        with ARTIFACT.open('rb') as src:
            while block:=src.read(1024*1024):
                self.wfile.write(block);total+=len(block)
                if time.monotonic()-last>=30:
                    print(now(),'transfer_bytes',total,'/',ARTIFACT.stat().st_size,flush=True);last=time.monotonic()
        print(now(),'transfer_stream_complete',total,flush=True)
server=None;rc=1
try:
    (OWNER/'run.path').write_text(str(TREE/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
    record('start.json',{'utc':now(),'pid':os.getpid(),'issue':500,'scope':'authorized transfer and checksum-gated queue only'})
    with ARTIFACT.open('rb') as f: actual=hashlib.file_digest(f,'sha256').hexdigest()
    assert actual==SHA
    acceptance=json.loads(Path('/workspace/tmp/pixelelated-m7-h700-firmware-acceptance-01/artifacts/acceptance.json').read_text())
    assert acceptance['result']=='PASS' and acceptance['bundle']==str(BUNDLE)
    pre=readback('preflight.txt', '''set -e
printf 'boot_id='; cat /proc/sys/kernel/random/boot_id
cat /etc/os-release
printf 'model='; tr '\\000' '\\n' </proc/device-tree/model
printf 'dt_id='; tr '\\000' '\\n' </proc/device-tree/rocknix-dt-id
for p in /sys/class/regulator/*; do if [ "$(cat "$p/name" 2>/dev/null)" = vdd-dram ]; then printf 'dram_microvolts='; cat "$p/microvolts"; fi; done
printf 'battery_capacity='; cat /sys/class/power_supply/battery/capacity
printf 'battery_status='; cat /sys/class/power_supply/battery/status
printf 'external_power='; cat /sys/class/power_supply/axp20x-usb/online
df -k /storage /flash
mount | grep -E ' on /storage | on /flash | on /storage/roms '
ls -la /storage/.update
ps -eo pid,comm | grep -E 'retroarch|rclone|cloud|scrape|emulation' || true
''')
    assert 'Anbernic RG35XX SP' in pre and 'dram_microvolts=1100000' in pre and 'external_power=1' in pre
    assert 'BUILD_ID="69e6039f8fdbf971d3e6b694537f250036fdcd98"' in pre
    record('input.json',{'utc':now(),'artifact':str(ARTIFACT),'sha256':SHA,'bytes':ARTIFACT.stat().st_size,'remote_partial':REMOTE,'remote_queue':QUEUE,'expected_build_id':acceptance['distribution_commit']})
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
    port=server.server_address[1];threading.Thread(target=server.serve_forever,daemon=True).start()
    env=dict(os.environ,DEVICE_ACT_TIMEOUT='2400',DEVICE_ACT_SSH_OPTS=f'-o ExitOnForwardFailure=yes -R 127.0.0.1:{port}:127.0.0.1:{port}')
    command=f'''set -e
[ "$(tr -d '\\000' </proc/device-tree/rocknix-dt-id)" = sun50i-h700-anbernic-rg35xx-sp ]
[ "$(cat /sys/class/power_supply/axp20x-usb/online)" = 1 ]
[ -z "$(find /storage/.update -mindepth 1 -maxdepth 1 -print -quit)" ]
[ ! -e '{REMOTE}' ]
[ "$(df -Pk /storage | tail -1 | awk '{{print $4}}')" -gt 3000000 ]
if ps -eo comm | grep -E '^(retroarch.*|rclone|cloud_.*|scraper)$'; then echo 'REFUSED active game or cloud process'; exit 20; fi
if [ -e /var/run/cloud_sync.lock ]; then flock -n /var/run/cloud_sync.lock true; fi
curl --fail --silent --show-error --max-time 1800 'http://127.0.0.1:{port}/firmware.tar' --output '{REMOTE}'
printf 'download_bytes='; stat -c %s '{REMOTE}'
actual=$(sha256sum '{REMOTE}' | cut -d ' ' -f1)
printf 'device_sha256=%s\\n' "$actual"
[ "$actual" = '{SHA}' ]
[ -z "$(find /storage/.update -mindepth 1 -maxdepth 1 -print -quit)" ]
mv '{REMOTE}' '{QUEUE}'
sync
printf 'STAGED verified update\\n'
printf 'battery_capacity='; cat /sys/class/power_supply/battery/capacity
printf 'battery_status='; cat /sys/class/power_supply/battery/status
printf 'external_power='; cat /sys/class/power_supply/axp20x-usb/online
'''
    r=subprocess.run([str(TREE/'tools/device-act'),'rg35xxsp','M7 #500 transfer and checksum-gated queue H700 43d0bc3bf4','--',command],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    output=filtered(r.stdout);(OWNER/'transfer.log').write_text(output);print(output,flush=True)
    assert r.returncode==0 and 'STAGED verified update' in output and 'device_sha256='+SHA in output
    record('stage-result.json',{'utc':now(),'result':'PASS','remote_sha256':SHA,'queue':QUEUE,'rebooted':False})
    rc=0
except Exception as error:
    record('stage-error.json',{'utc':now(),'type':type(error).__name__,'message':str(error)})
    print(type(error).__name__,str(error),flush=True)
finally:
    if server:server.shutdown();server.server_close()
    for name in ['inner.rc','outer.rc']:(OWNER/name).write_text(str(rc)+'\n')
raise SystemExit(rc)
