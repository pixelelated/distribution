from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,socket,subprocess,time
owner=Path('/workspace/tmp/pixelelated-m7-copy-transport-control-02');owner.mkdir()
data=owner/'data';data.mkdir();source=data/'source';source.mkdir();(source/'witness').write_bytes(b'0123456789abcdef'*524288)
client=Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement15/build.pixelelated-GENERIC_X64.x86_64/image/system/usr/bin/rclone')
assert client.is_file()
with socket.socket() as s:s.bind(('127.0.0.1',9046))
serverlog=(owner/'server.log').open('w');server=subprocess.Popen(['/usr/bin/rclone','serve','webdav',str(data),'--addr','127.0.0.1:9046','--dir-cache-time','1s','--config','/dev/null','-vv'],stdout=serverlog,stderr=subprocess.STDOUT)
copy=None;started=time.monotonic();result={}
try:
    for _ in range(100):
        try:
            with socket.create_connection(('127.0.0.1',9046),timeout=.2):break
        except OSError:time.sleep(.05)
    else:raise AssertionError('server did not start')
    config=owner/'rclone.conf';config.write_text('[qa]\ntype=webdav\nurl=http://127.0.0.1:9046\nvendor=other\n');remote='qa:'
    base=[str(client),'copy',remote+'source',remote+'default','--config',str(config),'--bwlimit','256k','-vv']
    t=time.monotonic();r=subprocess.run(base,text=True,capture_output=True,timeout=8)
    (owner/'default.log').write_text(r.stdout+r.stderr)
    assert r.returncode==0 and 'server-side copy' in r.stderr,r.stderr
    assert (data/'default/witness').read_bytes()==(source/'witness').read_bytes()
    result['default']={'returncode':r.returncode,'seconds':time.monotonic()-t,'server_side_copy_log':True,'destination_bytes':(data/'default/witness').stat().st_size}
    args=[str(client),'copy',remote+'source',remote+'streamed','--config',str(config),'--bwlimit','256k','--disable','copy','-vv']
    with (owner/'streamed.log').open('w') as f:
        copy=subprocess.Popen(args,stdout=f,stderr=subprocess.STDOUT)
        partial=None
        for _ in range(100):
            p=data/'streamed/witness'
            if p.is_file() and 0<p.stat().st_size<(source/'witness').stat().st_size:
                partial={'path':str(p),'bytes':p.stat().st_size,'source_bytes':(source/'witness').stat().st_size,'pid':copy.pid,'argv':args};break
            assert copy.poll() is None,'streaming copy ended before observer'
            time.sleep(.05)
        result['streamed']={'partial':partial,'observed_files':{str(p.relative_to(data)):p.stat().st_size for p in data.rglob('*') if p.is_file()}}
        assert partial is not None,result
        copy.terminate();copy.wait(timeout=5)
        result['streamed']['control_termination_rc']=copy.returncode
    result.update(utc=datetime.now(timezone.utc).isoformat(),client_sha256=hashlib.sha256(client.read_bytes()).hexdigest(),client_version=subprocess.check_output([str(client),'version'],text=True),server_version=subprocess.check_output(['/usr/bin/rclone','version'],text=True),scope='Host transport control using actual installed candidate15 client and same host WebDAV server binary. No installed UI acceptance claim.')
finally:
    if copy and copy.poll() is None:copy.kill();copy.wait(timeout=5)
    server.terminate();server.wait(timeout=5);serverlog.close()
    assert not Path('/proc',str(server.pid)).exists()
    if copy:assert not Path('/proc',str(copy.pid)).exists()
    with socket.socket() as s:s.bind(('127.0.0.1',9046))
    result['cleanup']={'server_pid_absent':server.pid,'client_pid_absent':copy.pid if copy else None,'port9046_free':True,'seconds':time.monotonic()-started}
    (owner/'control.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
