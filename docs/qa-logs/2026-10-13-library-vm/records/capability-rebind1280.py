from pathlib import Path
import json,time,subprocess
from ui import out,remote
r=Path(__file__).parent
p=json.loads((r/'records/capability-preparation.json').read_text())
remote('systemctl stop essway.service',capture_output=True)
assert out('sha256sum /usr/config/emulationstation/es_systems.cfg').split()[0]==p['original_systems_sha256']
assert out('sha256sum /storage/qa575/es_systems.cfg').split()[0]==p['staged_systems_sha256']
assert out('cat /storage/qa575/launch-events')==''
remote('mount --bind /storage/qa575/es_systems.cfg /usr/config/emulationstation/es_systems.cfg; mount --make-private /usr/config/emulationstation/es_systems.cfg; mount --bind /storage/qa575/no-launch /usr/bin/runemu.sh; mount --make-private /usr/bin/runemu.sh',capture_output=True)
(r/'records/capability-rebind1280.json').write_text(json.dumps({'rc':0,'boot':out('cat /proc/sys/kernel/random/boot_id').strip(),'identities':out('sha256sum /usr/config/emulationstation/es_systems.cfg /usr/config/emulationstation/es_features.cfg /usr/config/emulationstation/es_savestates.cfg /usr/bin/runemu.sh')},indent=2)+'\n')
