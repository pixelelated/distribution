import subprocess,time,json,pathlib
O=pathlib.Path('/workspace/tmp/pixelelated-510-coverage02/fault-settings-changed01')
SSH=['ssh','-i','/workspace/tmp/pixelelated-510-coverage02/guest01/qa-key','-p','10212','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','root@127.0.0.1']
V=['python3','/workspace/repos/rocknix.worktrees/conflict-resolution/tools/vm-visual-qa','--monitor','/tmp/pix512-mon.sock']
def ssh(c):
 r=subprocess.run(SSH+[c],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=True);print(r.stdout,flush=True);return r.stdout
before=ssh('cloud_setup --validation-context; find /storage/qa512/provider -type f')
ssh('kill -STOP "$(cat /storage/qa512/provider.pid)"')
try:
 subprocess.run(V+['key','x'],check=True)
 for _ in range(30):
  if 'rclone' in ssh("ps -eo args | awk '/^rclone (lsf|lsjson|lsd)/ {print}'"):break
  time.sleep(.2)
 else:raise RuntimeError('network phase not reached')
 ssh("sed -i 's|^SETTINGS_REMOTE=.*|SETTINGS_REMOTE=\"/pixelelated/Backups-change\"|' /storage/.config/cloud_sync.conf")
finally:ssh('kill -CONT "$(cat /storage/qa512/provider.pid)"')
subprocess.run(V+['settle'],check=True)
time.sleep(3)
subprocess.run(V+['shot',str(O/'frames/settings-changed-unfixed.png')],check=True)
after=ssh('cloud_setup --validation-context; find /storage/qa512/provider -type f; tail -n 12 /storage/.config/emulationstation/es_log.txt')
(O/'receipt.json').write_text(json.dumps({'before':before,'after':after,'fixture':'synthetic config changes while real metadata scan is blocked'},indent=2))
