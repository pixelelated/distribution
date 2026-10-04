import pathlib, re, subprocess, sys
root = pathlib.Path(sys.argv[1])
script = root / 'projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout'
r = subprocess.run(['bash', str(script), '--superseded'], capture_output=True, text=True, check=True)
old = [x.lstrip('/') for x in r.stdout.splitlines() if x.startswith('/')]
if not old:
    raise SystemExit('no superseded defaults read')
patterns = [re.compile(r'(?<![\w-])/?' + re.escape(x) + r'(?=/|[\s\"\']|$)') for x in old]
for name in ['vm-qa','cloud-test-backend','cloud-round-trip','vm-upgrade-rehearsal','time-to-play','cloud-pair-migration']:
    for line_no, line in enumerate((root/'tools'/name).read_text().splitlines(), 1):
        if line.lstrip().startswith('#'):
            continue
        if any(p.search(line) for p in patterns):
            print(f'{name}:{line_no}: superseded folder literal')
# An inline comment must not hide the live path before it.
assert any(p.search('path="/' + old[0] + '" # history') for p in patterns)
# #366: verify every advertised backend's actual derived path, without starting it.
backend_tool = str(root / 'tools/cloud-test-backend')
def backend_query(*args):
    return subprocess.check_output([backend_tool, *args], text=True).strip()
backends = backend_query('backends').split()
assert backends and len(backends) == len(set(backends)), 'empty/duplicate backend list'
default = backend_query('shipped-default', 'SAVES_REMOTE')
assert default.startswith('/') and not any(p.search(default) for p in patterns)
for backend in backends:
    prefix = backend_query('--backend', backend, 'endpoint-prefix')
    remote = backend_query('--backend', backend, 'saves-remote')
    assert remote == prefix + default, f'{backend}: prefix/default mismatch'
    assert not any(p.search(remote) for p in patterns), f'{backend}: superseded path'
    if backend == 's3':
        bucket = prefix.removeprefix('/')
        assert re.fullmatch(r'[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]', bucket), 'illegal S3 bucket'
        assert '..' not in bucket and not re.fullmatch(r'[0-9]+(?:\.[0-9]+){3}', bucket)
