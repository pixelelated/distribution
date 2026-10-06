"""Read exact installed identity, policy, script and Ocean bytes in an isolated guest."""
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys

owner = Path('/workspace/tmp/pixelelated-m7-ra-ui-03')


def guest(command):
    return subprocess.check_output(['ssh','-i',str(owner/'pair/qa-key'),'-p','10026','-o','BatchMode=yes','-o','ConnectTimeout=8','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=/dev/null','-o','LogLevel=ERROR','root@127.0.0.1',command], text=True).strip()


expected = '7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2'
bid = guest("sed -n 's/^BUILD_ID=//p' /etc/os-release").strip('"')
assert bid == expected, bid
assert guest("sed -n 's/^OS_NAME=//p' /etc/os-release").strip('"') == 'pixelelated'
assert guest("sed -n 's/^BUILD_BRANCH=//p' /etc/os-release").strip('"') == 'build/m7-pixelelated-replacement14'
mapping = {f'/usr/share/licenses/pixelelated/{name}': (Path(name), '644')
           for name in ['LICENSE.md', 'TRADEMARK.md']}
mapping.update({f'/usr/bin/{name}': (Path('projects/ROCKNIX/packages/network/rclone/sources') / name, '755')
                for name in ['cloud_content_backup', 'cloud_content_restore', 'cloud_content_transfer',
                             'cloud_backup', 'cloud_restore', 'cloud_migrate_layout']})
mapping['/usr/bin/raofflineproxy-ctl'] = (Path('projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl'), '755')
mapping['/etc/profile.d/001-functions'] = (Path('projects/ROCKNIX/packages/rocknix/profile.d/001-functions'), '644')
mapping['/usr/bin/chksysconfig'] = (Path('projects/ROCKNIX/packages/rocknix/sources/scripts/chksysconfig'), '755')
wordmark = Path('projects/ROCKNIX/packages/ui/themes/es-theme-art-book-next/sources/pixelelated-wordmark.svg')
for remote in ['/usr/config/emulationstation/resources/pixelelated-wordmark.svg',
               '/usr/share/themes/es-theme-art-book-next/pixelelated-wordmark.svg']:
    mapping[remote] = (wordmark, '644')
mapping['/usr/config/modules/gamelist.xml'] = (Path('projects/ROCKNIX/packages/misc/modules/sources/gamelist.xml'), '644')
mapping['/usr/bin/cloud_setup'] = (Path('projects/ROCKNIX/packages/network/rclone/sources/cloud_setup'), '755')
mapping['/usr/bin/rocknix-memory-manager'] = (Path('projects/ROCKNIX/packages/rocknix/sources/scripts/rocknix-memory-manager'), '755')
mapping['/etc/profile.d/999-export'] = (Path('projects/ROCKNIX/packages/hardware/quirks/profile.d/999-export'), '755')
proof = {}
for remote, (local, wanted_mode) in mapping.items():
    line = guest('sha256sum ' + shlex.quote(remote))
    wanted = hashlib.sha256(local.read_bytes()).hexdigest()
    assert line.split()[0] == wanted, (remote, line)
    mode = guest("stat -c '%a' " + shlex.quote(remote))
    assert mode == wanted_mode, (remote, mode)
    proof[remote] = {'sha256': wanted, 'mode': mode}
# Select only the application identity field; never expose other environment values.
import time
for attempt in range(90):
    pids=guest('pidof emulationstation || true').split()
    if len(pids)==1 and pids[0].isdigit():
        es_pid=pids[0]
        es_exe=guest('readlink /proc/'+es_pid+'/exe')
        if es_exe=='/usr/bin/emulationstation':break
    time.sleep(1)
else:raise AssertionError('one running installed ES process required')
es_name=guest("tr '\\0' '\\n' < /proc/"+es_pid+"/environ | sed -n '/^OS_NAME=/p'")
assert es_name=='OS_NAME=pixelelated',(es_pid,es_name)
proof['running_emulationstation']={'pid':int(es_pid),'exe':es_exe,'OS_NAME':'pixelelated'}
out = {'phase': sys.argv[1], 'build_id': bid, 'os_name': 'pixelelated', 'files': proof, 'passed': True}
(owner / 'artifacts' / ('payload-' + sys.argv[1] + '.json')).write_text(json.dumps(out, indent=2) + '\n')
print('PASS ' + sys.argv[1] + ' exact identity, installed scripts, policy and Ocean SVG bytes/modes')

proxy_code = (owner / 'proxy-identity.py').read_text()
proxy_result = json.loads(guest("python3 - <<'PROXY_IDENTITY'\n" + proxy_code + "\nPROXY_IDENTITY"))
assert proxy_result['passed']
(owner / 'artifacts' / ('proxy-identity-' + sys.argv[1] + '.json')).write_text(json.dumps(proxy_result, indent=2) + '\n')
print('PASS ' + sys.argv[1] + ' installed proxy identities and account discovery')
