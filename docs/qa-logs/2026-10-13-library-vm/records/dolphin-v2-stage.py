from pathlib import Path
import json,hashlib
from ui import out,remote
r=Path(__file__).parent;s=json.loads((r/'records/dolphin-installed-v2-source.json').read_text());src='/tmp/pix581-v2-source';defaults='/tmp/pix581-v2-defaults'
remote('mkdir '+src+' '+defaults,capture_output=True)
for name,target in [('dolphin-installed-v2.tar',src+'/source.tar'),('dolphin-packaged-defaults.tar.gz',defaults+'/defaults.tar.gz'),('dolphin-packaged-defaults.json',defaults+'/receipt.json')]:
 p=r/'records'/name
 with p.open('rb') as f:remote('cat > '+target,stdin=f)
 assert out('sha256sum '+target).split()[0]==hashlib.sha256(p.read_bytes()).hexdigest()
remote('tar xf '+src+'/source.tar -C '+src+' && tar xpf '+defaults+'/defaults.tar.gz -C '+defaults,capture_output=True)
result=out('python3 -I -S -B '+src+'/'+s['packet']+'/installed_flow.py stage-products --repo '+src+' --renderer Vulkan --output /tmp/pix581-v2-products')
(r/'dolphin-v2-stage-result.json').write_text(json.dumps({'rc':0,'stdout':result,'source':s},indent=2)+'\n')
