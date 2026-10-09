import pathlib,subprocess,time,json,urllib.request,os,signal,socket,hashlib
O=pathlib.Path('/tmp/pix529-fixed');O.mkdir(exist_ok=False)
DROP=pathlib.Path('/run/systemd/system/sway.service.d/529-delay.conf')
OVERRIDE=pathlib.Path('/storage/.config/profile.d/099-qa-readiness')
results=[]
def run(a,check=True,timeout=25):
 r=subprocess.run(a,capture_output=True,text=True,timeout=timeout)
 if check and r.returncode:raise RuntimeError((a,r.returncode,r.stdout,r.stderr))
 return r
def shell(s,**kw):return run(['/bin/bash','-c',s],**kw)
def idle():
 try:return json.load(urllib.request.urlopen('http://127.0.0.1:1234/isIdle',timeout=.3))==[True]
 except Exception:return False
def cursor():return run(['journalctl','-n','0','--show-cursor']).stdout.split('-- cursor: ')[1].strip()
def journal(c):return run(['journalctl','--after-cursor',c,'-u','essway.service','-u','sway.service','-o','short-monotonic','--no-pager']).stdout
def save(name,obj):
 (O/(name+'.json')).write_text(json.dumps(obj,indent=2)+'\n')
 results.append(obj);print(json.dumps(obj),flush=True)
def launch_case(name,delay):
 run(['systemctl','stop','essway.service','sway.service'])
 DROP.parent.mkdir(parents=True,exist_ok=True)
 DROP.write_text('[Service]\nExecStart=\nExecStart=/bin/sh -c "sleep '+str(delay)+'; exec /usr/bin/sway.sh"\n')
 run(['systemctl','daemon-reload']);run(['systemctl','reset-failed','essway.service','sway.service'])
 c=cursor();start=time.monotonic();run(['systemctl','--no-block','start','essway.service'])
 timeline=[]
 while time.monotonic()-start < 50:
  state=run(['systemctl','show','essway.service','-p','SubState','-p','NRestarts','-p','MainPID']).stdout
  ready=idle();timeline.append({'elapsed':round(time.monotonic()-start,3),'state':state,'idle':ready})
  if ready:break
  time.sleep(.1)
 assert ready,(name,'idle timeout')
 j=journal(c);(O/(name+'-journal.txt')).write_text(j);(O/(name+'-timeline.json')).write_text(json.dumps(timeline,indent=2)+'\n')
 n=int(run(['systemctl','show','essway.service','-p','NRestarts','--value']).stdout)
 assert 'Error initializing SDL!' not in j,(name,j)
 assert n==0 if delay<15 else n>=1,(name,n)
 assert ('sway-ready: timed out' in j)==(delay>=15)
 save(name,{'case':name,'delay_seconds':delay,'idle_seconds':timeline[-1]['elapsed'],'restarts':n,'sdl_errors':0,'timeout_diagnostic': 'sway-ready: timed out' in j,'passed':True})
 return j
# Exact proposed unit and helper were uploaded/bound by the host; immutable OS
# remains the accepted image. The unit override points ExecStartPre at /tmp.
launch_case('fixed-default',0)
launch_case('fixed-delayed',8)
launch_case('fixed-late-recovery',22)
# Direct helper failure controls use the actual production deadline and tools.
run(['systemctl','stop','essway.service'])
def helper_case(name,ok):
 t=time.monotonic();r=run(['/tmp/pix529-sway-ready'],check=False,timeout=22);elapsed=time.monotonic()-t
 (O/(name+'-stderr.txt')).write_text(r.stderr)
 assert (r.returncode==0)==ok,(name,r.returncode,r.stdout,r.stderr)
 if not ok:assert 13 <= elapsed <= 19 and 'timed out' in r.stderr,(name,elapsed,r.stderr)
 else:assert elapsed < 2,(name,elapsed)
 save(name,{'case':name,'returncode':r.returncode,'elapsed':round(elapsed,3),'passed':True})
helper_case('responsive',True)
OVERRIDE.write_text('export WAYLAND_DISPLAY=/tmp/pix529-absent-wayland\n')
try:helper_case('absent-wayland',False)
finally:OVERRIDE.unlink()
# A socket inode without a server must not qualify against the real Sway IPC.
s=socket.socket(socket.AF_UNIX);s.bind('/tmp/pix529-stale-wayland');s.close()
OVERRIDE.write_text('export WAYLAND_DISPLAY=/tmp/pix529-stale-wayland\n')
try:helper_case('stale-wayland',False)
finally:OVERRIDE.unlink();pathlib.Path('/tmp/pix529-stale-wayland').unlink()
# A real but nonresponsive compositor must time out even though sockets exist.
pids=[int(p.name) for p in pathlib.Path('/proc').iterdir() if p.name.isdigit() and (p/'comm').exists() and (p/'comm').read_text().strip()=='sway']
assert len(pids)==1,pids
os.kill(pids[0],signal.SIGSTOP)
try:helper_case('hung-compositor',False)
finally:os.kill(pids[0],signal.SIGCONT)
helper_case('recovered-compositor',True)
# No active output cannot qualify even when both protocols answer.
shell('. /etc/profile >/dev/null 2>&1; swaymsg "output * disable"')
try:helper_case('no-active-output',False)
finally:shell('. /etc/profile >/dev/null 2>&1; swaymsg "output * enable"')
helper_case('restored-output',True)
# Absolute display paths supported by Wayland remain supported by the guard.
OVERRIDE.write_text('export WAYLAND_DISPLAY=/var/run/0-runtime-dir/wayland-1\n')
try:helper_case('absolute-wayland-path',True)
finally:OVERRIDE.unlink()
DROP.unlink();run(['systemctl','daemon-reload']);run(['systemctl','start','essway.service'])
t=time.monotonic()
while not idle() and time.monotonic()-t<20:time.sleep(.1)
assert idle()
save('summary',{'case':'summary','controls_passed':len(results),'original_image_unchanged':True,'runtime_overlay':True,'terminal_idle':True,'passed':True})
