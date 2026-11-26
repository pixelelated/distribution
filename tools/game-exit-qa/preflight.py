"""Gate the selected one-exit case on the sealed backend's actual guest preflight."""
import base64
import json
import re
import time

from common import write
import menu_timing as T


FAMILIES = ('-4', '-6')
PREFIX = 'M7_1433_BACKEND_PREFLIGHT='
BACKEND = '/tmp/m7-1433-armed-input/backend.py'


def client_snapshot(ctx, label, child=None):
    child_check = ''
    if child is not None:
        pid, ns = child
        assert type(pid) is int and pid > 1
        assert re.fullmatch(r'net:\[\d+\]', ns)
        child_check = f'test "$(readlink /proc/{pid}/ns/net 2>/dev/null || :)" != "{ns}"'
    data, rc = ctx.serial(label, f'''
set -eu
printf 'CLIENT_NS='; readlink /proc/self/ns/net
printf 'LINKS='; ls /sys/class/net
test "$(ls /sys/class/net)" = lo
for f in -4 -6; do
  printf 'ALL_TABLES=%s\n' "$f"
  /usr/bin/busybox ip "$f" route show table all
done
v4=$(/usr/bin/busybox ip -4 route show table all to exact 0.0.0.0/0)
v6=$(/usr/bin/busybox ip -6 route show table all to exact ::/0)
printf 'EXACT_V4_DEFAULT=%s\nEXACT_V6_DEFAULT=%s\n' "$v4" "$v6"
test -z "$v4"
test -z "$v6"
{child_check}
''', 15)
    namespaces = [line.removeprefix('CLIENT_NS=') for line in data.splitlines()
                  if line.startswith('CLIENT_NS=')]
    defaults_absent = all([line for line in data.splitlines() if line.startswith(prefix)] == [prefix]
                          for prefix in ('EXACT_V4_DEFAULT=','EXACT_V6_DEFAULT='))
    return {'rc':rc,'namespace':namespaces[0] if len(namespaces)==1 else None,
            'defaults_absent':defaults_absent}


def observed(row):
    raw = {k: base64.b64decode(row[k+'_base64'], validate=True) for k in ('stdout','stderr')}
    assert all(len(x) <= 2048 for x in raw.values()), 'guest namespace stream cap'
    assert row['original_rc'] == 0 and not row['timed_out'] and not row['output_capped'], 'guest namespace original command'
    assert not raw['stderr'] and not row.get('cleanup_error') and not row.get('error'), 'guest namespace stderr/cleanup'
    return raw['stdout']


def snapshot(rows, peer):
    assert set(rows) == set(FAMILIES), 'both route families'
    parsed = {}
    for family in FAMILIES:
        row = rows[family]
        census = observed(row['route_table_all'])
        exact = observed(row['route_exact_default'])
        defaults = {b'default', b'0.0.0.0/0', b'::/0', b'0/0'}
        assert not exact.strip() and not any(defaults.intersection(line.split()[:2]) for line in census.splitlines()), family+' backend default'
        assert row['default_present'] is False
        base = '/proc/sys/net/'+('ipv4' if family == '-4' else 'ipv6')
        global_path = base+('/ip_forward' if family == '-4' else '/conf/all/forwarding')
        assert row['forwarding_paths'] == [global_path,base+f'/conf/{peer}/forwarding',base+'/conf/lo/forwarding']
        flags = observed(row['forwarding']).splitlines()
        assert len(flags)==3 and all(x in (b'0',b'1') for x in flags), family+' forwarding bytes'
        parsed[family] = [int(x) for x in flags]
        assert row['forwarding_values'] == parsed[family]
    return parsed


def verify_report(row, boot, attempt):
    assert row['boot_id'] == boot and row['attempt'] == attempt
    assert row['status'] == 'ISOLATED_PREFLIGHT_COMPLETE'
    assert row['preflight_busybox'] == {'bytes':578560,'sha256':'1635ba7a93496fbdde8cf946d94b6d6963cd9110bdb81657cdf30e95ea28ac5c'}
    assert row['backend_cleanup_errors'] == [] and row['backend_cleanup']['original_rc'] == -15
    assert row['backend_cleanup']['sent'] == 'TERM' and 'backend' not in row, 'WebDAV must stay unstarted'
    report = row['backend_preflight']
    assert report['status'] == 'NO_DEFAULT_ROUTES_AND_FORWARDING_DISABLED'
    for kind in ('client','server'):
        assert report[kind+'_namespace'] == f"net:[{report[kind+'_kernel_identity'][1]}]"
    assert report['server_kernel_identity'] != report['client_kernel_identity']
    r = report['before']['-4']['forwarding_paths'][1]
    peer = r.split('/')[-2]
    assert peer not in ('lo','m7qa1433') and re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_.-]{0,14}', peer)
    before = snapshot(report['before'], peer)
    writes = report['writes']
    assert set(writes) == {f for f in FAMILIES if before[f][0] == 1}, 'write only observed enabled global'
    for family, command in writes.items():
        assert observed(command) == b'' and command['argv'][-1] == report['before'][family]['forwarding_paths'][0]
    assert ('after' in report) == bool(writes)
    final = snapshot(report['after'], peer) if writes else before
    assert final == {f:[0,0,0] for f in FAMILIES}, 'final global/peer/lo forwarding'
    return {'before_forwarding':before,'final_forwarding':final,'writes':sorted(writes),
            'after_source':'after' if writes else 'before, no write required','peer':peer}


def execute(ctx, owner, boot, attempt, deadline):
    assert deadline-time.monotonic()>T.PREFLIGHT+T.WITNESS_STAGE+T.ARM_AND_ARCHIVE, 'preflight and reserved arm/archive budget'
    observation = {'boot_id':boot,'attempt':attempt,'original_guest_rc':None,
                   'status':'REFUSED_OR_INCOMPLETE','armed_permitted':False}
    try:
        before = observation['client_before'] = client_snapshot(ctx,'1433-preflight-client-before')
        assert before['rc']==0 and before['defaults_absent'], 'initial no-uplink client check'
        body, rc = ctx.serial('1433-backend-preflight-only',
                              f'python3 -I -B {BACKEND} --preflight-only-disposable-no-nic --boot-id {boot} --attempt {attempt}',120)
        observation['original_guest_rc'] = rc
        lines = [line[len(PREFIX):] for line in body.splitlines() if line.startswith(PREFIX)]
        observation['result_lines'] = len(lines)
        row = None
        if len(lines)==1 and len(lines[0])<=96*1024:
            row = json.loads(lines[0])
            write(owner/'records/1433-backend-preflight.json',row,True)
        report = (row or {}).get('backend_preflight',{})
        child = (report['server_pid'],report['server_namespace']) if 'server_pid' in report else None
        after = observation['client_after'] = client_snapshot(ctx,'1433-preflight-client-after',child)
        assert rc == 0, (row or {}).get('error','preflight original refused or unknown')
        assert row is not None, 'exactly one bounded backend preflight result'
        observation.update(verify_report(row,boot,attempt))
        assert after['rc']==0 and after['defaults_absent'], 'retired-server/no-uplink client check'
        assert after['namespace']==before['namespace']==report['client_namespace'], 'same guest client namespace'
        assert deadline-time.monotonic()>T.WITNESS_STAGE+T.ARM_AND_ARCHIVE, 'witness stage and reserved arm/archive budget'
        observation.update(status='AFFIRMATIVE_ISOLATION_AND_CLEANUP',armed_permitted=True)
    except BaseException as error:
        observation['error'] = type(error).__name__+': '+str(error)
        raise
    finally:
        write(owner/'records/1433-backend-gate.json',observation,True)
