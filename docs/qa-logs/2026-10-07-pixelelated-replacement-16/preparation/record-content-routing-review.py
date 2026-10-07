from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import struct
import sys

source=Path('/workspace/tmp/pixelelated-m7-p4-build16-content-routing-640x480-01/artifacts/cloud-ui')
receipt=Path('.build-runs/content-routing01-frame-review.json')
request=json.load(sys.stdin)
rows=json.loads(receipt.read_text()) if receipt.exists() else []
known={row['file']:row for row in rows}
for name in request['files']:
    assert Path(name).name==name
    data=(source/name).read_bytes()
    assert data[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',data[16:24])==(640,480)
    digest=hashlib.sha256(data).hexdigest()
    if name in known:
        assert known[name]['sha256']==digest
        continue
    rows.append(dict(file=name,sha256=digest,dimensions=[640,480],result='PASS',primary_direct_review=True,reviewed_utc=datetime.now(timezone.utc).isoformat(),observation=request['observation']))
receipt.write_text(json.dumps(rows,indent=2)+'\n')
print(len(rows),'directly reviewed routing frames recorded')
