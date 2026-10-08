"""Prepare-only restart procedure. Run only after root releases host resources."""
import pathlib,subprocess,json,time,hashlib
b=pathlib.Path('/workspace/tmp/pixelelated-520-ui-20261008');o=b/'restart01';o.mkdir(exist_ok=False)
receipt=json.loads((b/'maintenance-stop01/receipt.json').read_text());assert receipt['process_exited'];assert pathlib.Path(receipt['disk_preserved']).is_file()
subprocess.run(receipt['restart_command'],check=True);pid=int((b/'guest01/vm.pid').read_text());print('QEMU newPID',pid,flush=True)
ssh=['ssh','-i',str(b/'guest01/qa-key'),'-p','10220','-o','ConnectTimeout=3','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','root@127.0.0.1'];start=time.monotonic()
while True:
 q=subprocess.run(ssh+['true'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if q.returncode==0:break
 if time.monotonic()-start>90:raise RuntimeError('Same guest SSH startup exceeded90s')
 time.sleep(2)
cmd='''set -eu
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
''';(o/'rebind.sh').write_text(cmd);q=subprocess.run(ssh+[cmd],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(o/'rebind.log').write_bytes(q.stdout);print(q.stdout.decode(),flush=True);q.check_returncode()
m=json.loads((b/'backend01/install-manifest.json').read_text());cmd='sha256sum '+' '.join(x['destination'] for x in m['installed_files']);raw=subprocess.check_output(ssh+[cmd]);(o/'cloud-installed-sha256.txt').write_bytes(raw);actual={line.split()[1]:line.split()[0] for line in raw.decode().splitlines()};assert all(actual[x['destination']]==x['sha256'] for x in m['installed_files']);(o/'restart.json').write_text(json.dumps({'new_qemu_pid':pid,'ssh_ready_seconds':time.monotonic()-start,'same_disk':receipt['disk_preserved'],'guest_es_state':'stopped for521native runtime; no520test repeated','cloud22_hashes_match':True,'dependency_overlay':'not yet applied by restart procedure'},indent=2)+'\n');print('PASS same guest restarted; exact frozen overlays restored; ES held stopped for native fixture',flush=True)
