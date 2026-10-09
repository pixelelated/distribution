import pathlib,subprocess,time,json,urllib.request
O=pathlib.Path('/tmp/pix529-baseline');O.mkdir(exist_ok=False)
def run(a,check=True):
 r=subprocess.run(a,capture_output=True,text=True,timeout=20)
 if check and r.returncode:raise RuntimeError((a,r.returncode,r.stderr))
 return r
run(['systemctl','stop','essway.service','sway.service'])
p=pathlib.Path('/run/systemd/system/sway.service.d/529-delay.conf');p.parent.mkdir(parents=True,exist_ok=True)
p.write_text('[Service]\nExecStart=\nExecStart=/bin/sh -c "sleep 8; exec /usr/bin/sway.sh"\n')
run(['systemctl','daemon-reload']);run(['systemctl','reset-failed','essway.service','sway.service'])
cursor=run(['journalctl','-n','0','--show-cursor']).stdout.split('-- cursor: ')[1].strip()
start=time.monotonic();run(['systemctl','--no-block','start','essway.service']);timeline=[]
for i in range(240):
 state=run(['systemctl','show','essway.service','sway.service','-p','ActiveState','-p','SubState','-p','NRestarts','-p','MainPID']).stdout
 ready=False
 try:ready=json.load(urllib.request.urlopen('http://127.0.0.1:1234/isIdle',timeout=.3))==[True]
 except Exception:pass
 timeline.append({'elapsed':round(time.monotonic()-start,3),'wayland_socket':pathlib.Path('/var/run/0-runtime-dir/wayland-1').exists(),'state':state,'idle':ready})
 if ready:break
 time.sleep(.15)
else:raise RuntimeError('ES did not recover in delayed original case')
journal=run(['journalctl','--after-cursor',cursor,'-u','essway.service','-u','sway.service','-o','short-monotonic','--no-pager']).stdout
assert 'Error initializing SDL!' in journal and 'wayland not available' in journal
assert 'Scheduled restart job' in journal
(O/'timeline.json').write_text(json.dumps(timeline,indent=2)+'\n');(O/'journal.txt').write_text(journal)
result={'case':'original delayed compositor','delay_seconds':8,'first_idle_seconds':timeline[-1]['elapsed'],'sdl_failures':journal.count('Error initializing SDL!'),'terminal_idle':ready,'original_failure_retained':True}
(O/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
