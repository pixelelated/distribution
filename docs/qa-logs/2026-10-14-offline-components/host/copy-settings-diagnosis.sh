python3 -I -S -B - <<'INNER'
from pathlib import Path
import json
def parse(p):return dict(l.split('=',1) for l in Path(p).read_text().splitlines() if '=' in l and not l.lstrip().startswith('#'))
a=parse('/tmp/pix-output/copy-settings-before.cfg');b=parse('/storage/.config/system/configs/system.cfg');changes={k:{'before_present':k in a,'after_present':k in b,'before_empty':a.get(k)=='','after_empty':b.get(k)==''} for k in a.keys()|b.keys() if a.get(k)!=b.get(k)}
kept={k:{'before':a.get(k),'after':b.get(k)} for k in ['global.autosave','gamecube.autosave','dreamcast.autosave']};print(json.dumps({'changed_keys':changes,'preferences':kept,'no_launch':Path('/storage/qa575/launch-events').read_bytes()==b''},indent=2));assert all(v['before']==v['after'] for v in kept.values())
INNER
