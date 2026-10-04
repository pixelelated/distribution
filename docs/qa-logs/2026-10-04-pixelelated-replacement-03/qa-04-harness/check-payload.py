"""Read exact installed identity, policy, script and Ocean bytes in an isolated guest."""
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys

owner = Path('/workspace/tmp/pixelelated-m7-qa-04')


def guest(command):
    return subprocess.check_output(['./tools/vm-pair', 'ssh', 'a', command], text=True).strip()


expected = '02163b440bfb055531f50f30184327336a67f886'
bid = guest("sed -n 's/^BUILD_ID=//p' /etc/os-release").strip('"')
assert bid == expected, bid
assert guest("sed -n 's/^OS_NAME=//p' /etc/os-release").strip('"') == 'pixelelated'
assert guest("sed -n 's/^BUILD_BRANCH=//p' /etc/os-release").strip('"') == 'build/m7-pixelelated-replacement03'
mapping = {f'/usr/share/licenses/pixelelated/{name}': (Path(name), '644')
           for name in ['LICENSE.md', 'TRADEMARK.md']}
mapping.update({f'/usr/bin/{name}': (Path('projects/ROCKNIX/packages/network/rclone/sources') / name, '755')
                for name in ['cloud_content_backup', 'cloud_content_restore', 'cloud_content_transfer',
                             'cloud_backup', 'cloud_restore', 'cloud_migrate_layout']})
mapping['/usr/bin/raofflineproxy-ctl'] = (Path('projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl'), '755')
wordmark = Path('projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/sources/pixelelated-wordmark.svg')
for remote in ['/usr/config/emulationstation/resources/pixelelated-wordmark.svg',
               '/usr/share/themes/es-theme-art-book-next/pixelelated-wordmark.svg']:
    mapping[remote] = (wordmark, '644')
mapping['/usr/config/modules/gamelist.xml'] = (Path('projects/ROCKNIX/packages/misc/modules/sources/gamelist.xml'), '644')
mapping['/usr/bin/cloud_setup'] = (Path('projects/ROCKNIX/packages/network/rclone/sources/cloud_setup'), '755')
mapping['/usr/bin/rocknix-memory-manager'] = (Path('projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-memory-manager'), '755')
proof = {}
for remote, (local, wanted_mode) in mapping.items():
    line = guest('sha256sum ' + shlex.quote(remote))
    wanted = hashlib.sha256(local.read_bytes()).hexdigest()
    assert line.split()[0] == wanted, (remote, line)
    mode = guest("stat -c '%a' " + shlex.quote(remote))
    assert mode == wanted_mode, (remote, mode)
    proof[remote] = {'sha256': wanted, 'mode': mode}
out = {'phase': sys.argv[1], 'build_id': bid, 'os_name': 'pixelelated', 'files': proof, 'passed': True}
(owner / 'artifacts' / ('payload-' + sys.argv[1] + '.json')).write_text(json.dumps(out, indent=2) + '\n')
print('PASS ' + sys.argv[1] + ' exact identity, installed scripts, policy and Ocean SVG bytes/modes')
