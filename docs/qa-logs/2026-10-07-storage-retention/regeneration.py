from pathlib import Path
import datetime, gzip, hashlib, json, os, subprocess, sys, time
owner=Path(__file__).resolve().parent
(owner/'run.path').write_text(str(Path.cwd()/os.environ['RASTERATOPS_BUILD_RUN'])+'\n')
rc=1
try:
 for p,h in json.loads((owner/'seal.json').read_text()).items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
 bundle=Path('/workspace/artifacts/pixelelated-candidates/sha256/7f98f2d22985d11fe9c150015457894caf460104c9ce44abd16074167f23815a')
 name='pixelelated-GENERIC_X64.x86_64-0.0.1-from-ROCKNIX.img.gz'
 source=bundle/name;manifest=json.loads((bundle/'manifest.json').read_text())
 with source.open('rb') as f:
  h=hashlib.sha256()
  while block:=f.read(8*1024**2):h.update(block)
 assert h.hexdigest()==manifest['files'][name]['sha256']
 raw=owner/'scratch.raw';base=owner/'scratch-base.qcow2';overlay=owner/'scratch-overlay.qcow2'
 results=[];start=time.monotonic();total=0
 with gzip.open(source,'rb') as stream,raw.open('xb') as out:
  while block:=stream.read(1024**2):
   total+=len(block)
   if not block.strip(b'\0'):out.seek(len(block),1)
   else:out.write(block)
  out.truncate(total);out.flush();os.fsync(out.fileno())
 results.append({'operation':'decompress firmware to sparse raw disk','seconds':time.monotonic()-start,'logical_bytes':total,'allocated_bytes':raw.stat().st_blocks*512})
 print(json.dumps(results[-1]),flush=True)
 def run(command,label):
  start=time.monotonic();p=subprocess.run(command,capture_output=True,text=True);assert p.returncode==0,p.stderr
  result={'operation':label,'seconds':time.monotonic()-start,'argv':command,'stdout':p.stdout,'returncode':p.returncode};results.append(result);print(json.dumps(result),flush=True)
 run(['qemu-img','convert','-f','raw','-O','qcow2',str(raw),str(base)],'create standalone guest disk')
 run(['qemu-img','resize',str(base),'16G'],'resize guest to supported 16 GiB')
 run(['qemu-img','compare','-f','raw','-F','qcow2',str(raw),str(base)],'compare recreated guest contents to firmware')
 run(['qemu-img','create','-f','qcow2','-F','qcow2','-b',str(base),str(overlay)],'create disposable copy-on-write overlay')
 info=json.loads(subprocess.check_output(['qemu-img','info','--backing-chain','--output=json',str(overlay)],text=True))
 assert len(info)==2 and info[0]['full-backing-filename']==str(base)
 sizes={p.name:{'size':p.stat().st_size,'allocated_bytes':p.stat().st_blocks*512} for p in [raw,base,overlay]}
 # Only three exact, newly created benchmark files are removed. No retained guest is touched.
 for p in [overlay,base,raw]:assert p.parent==owner and p.is_file() and not p.is_symlink();p.unlink()
 assert not any(p.exists() for p in [raw,base,overlay])
 result={'result':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':str(source),'source_sha256':h.hexdigest(),'operations':results,'sizes':sizes,'scratch_removed':True,'scope':'One measurement on the current host; disk recreation only. No boot, test replay, old-state recreation or OS recompilation claimed.'}
 (owner/'artifacts/result.json').write_text(json.dumps(result,indent=2)+'\n');rc=0
finally:
 (owner/'inner.rc').write_text(str(rc)+'\n');(owner/'outer.rc').write_text(str(rc)+'\n')
sys.exit(rc)
