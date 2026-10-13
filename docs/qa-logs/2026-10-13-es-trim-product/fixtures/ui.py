from pathlib import Path
import subprocess,socket,time,json,sys
r=Path(__file__).parent;ssh=json.loads((r/'ssh-command.json').read_text())
def remote(c,**kw):return subprocess.run(ssh+[c],check=True,timeout=30,**kw)
def out(c):return remote(c,capture_output=True,text=True).stdout
def key(k):
 with socket.socket(socket.AF_UNIX) as s:
  s.settimeout(3);s.connect(str(r/'vm/monitor.sock'));s.recv(4096);s.sendall(('sendkey '+k+' 100\n').encode());time.sleep(.2);s.recv(4096)
def shot(p):
 remote("python3 - <<'P'\nimport os,subprocess\nfrom pathlib import Path\np=next(x for x in Path('/run').glob('**/wayland-*') if x.is_socket());e=dict(os.environ,XDG_RUNTIME_DIR=str(p.parent),WAYLAND_DISPLAY=p.name);subprocess.run(['grim','/storage/qa570product/frame.png'],env=e,check=True)\nP",capture_output=True)
 with Path(p).open('wb') as f:remote('cat /storage/qa570product/frame.png',stdout=f)
if __name__=='__main__':
 for k in sys.argv[1:-1]:key(k);time.sleep(.8)
 shot(r/sys.argv[-1])
