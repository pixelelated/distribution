import subprocess,time,json,pathlib
O=pathlib.Path('/workspace/tmp/pixelelated-510-coverage02/fault-settings-changed03')
SSH=['ssh','-i','/workspace/tmp/pixelelated-510-coverage02/guest01/qa-key','-p','10212','-o','LogLevel=ERROR','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','root@127.0.0.1']
V=['python3','/workspace/repos/rocknix.worktrees/conflict-resolution/tools/vm-visual-qa','--monitor','/tmp/pix512-mon.sock']
def ssh(c):
 r=subprocess.run(SSH+[c],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=True);print(r.stdout,flush=True);return r.stdout
ssh('systemctl restart essway.service')
time.sleep(2)
subprocess.run(V+['run',str(O/'open.txt'),'--outdir',str(O/'frames')],check=True)
before=ssh('cloud_setup --validation-context; find /storage/qa512/provider -type f')
ssh('rm -f /storage/.cache/cloud_sync/scan/started; kill -STOP "$(cat /storage/qa512/provider.pid)"')
try:
 subprocess.run(V+['key','x'],check=True)
 for _ in range(30):
  if 'STARTED' in ssh('test ! -f /storage/.cache/cloud_sync/scan/started || echo STARTED'):break
  time.sleep(.2)
 else:raise RuntimeError('network phase not reached')
 ssh("sed -i 's|^SETTINGS_REMOTE=.*|SETTINGS_REMOTE=\"/pixelelated/Backups-final\"|' /storage/.config/cloud_sync.conf")
finally:ssh('kill -CONT "$(cat /storage/qa512/provider.pid)"')
subprocess.run(V+['settle'],check=True)
time.sleep(3)
subprocess.run(V+['shot',str(O/'frames/settings-changed-fixed.png')],check=True)
after=ssh('cloud_setup --validation-context; find /storage/qa512/provider -type f; test ! -f /storage/.cache/cloud_sync/scan/done && echo NO-DONE-STAMP')
(O/'receipt.json').write_text(json.dumps({'before':before,'after':after,'fixture':'synthetic config changes while real metadata scan is blocked'},indent=2))

subprocess.run(V+['key','x'],check=True)
subprocess.run(V+['settle'],check=True)
time.sleep(2)
subprocess.run(V+['shot',str(O/'frames/settings-changed-retry.png')],check=True)
