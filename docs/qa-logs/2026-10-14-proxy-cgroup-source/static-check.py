#!/usr/bin/env python3
"""Static AST/hash/source inspection only. No prepared module imports or execution."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
sha = lambda raw: hashlib.sha256(raw).hexdigest()


def main():
    assert sys.flags.optimize == 0
    binding = json.loads((HERE/'compatibility.json').read_text())
    old = Path(binding['source_packet'])
    original_manifest = subprocess.run(['git','show',binding['parent_commit'] + ':docs/qa-logs/2026-10-14-proxy-service-source/SHA256SUMS'],
                                       capture_output=True,check=True,timeout=10).stdout
    assert original_manifest == (old/'SHA256SUMS').read_bytes()
    assert sha(original_manifest) == binding['parent_manifest_sha256']
    copied = []
    renamed = {'README.md':'prior-README.md','static-result.json':'prior-static-result.json'}
    for line in original_manifest.decode().splitlines():
        digest, name = line.split('  ',1)
        raw = (old/name).read_bytes(); assert sha(raw)==digest,name
        if name not in ('run.py','runner-seal.json'):
            assert (HERE/renamed.get(name,name)).read_bytes()==raw,name
            copied.append(name)
    before = (old/'run.py').read_text()
    expected = before.replace('global OUT, STATE, CENSUS, REF, UNIT_SHA, DROP_SHA',
                              'global OUT, STATE, CENSUS, REF, UNIT_SHA, DROP_SHA, CGROUP')
    needle = "        need(Path('/sys/fs/cgroup/cgroup.controllers').is_file(), 'cgroup v2 required for this bounded packet')"
    expected = expected.replace(needle,needle + "\n        CGROUP = module('service_cgroup_guard', PACKET / 'cgroup_guard.py')\n        REPORT['platform_contract'] = CGROUP.platform_contract(PACKET / 'compatibility.json')\n        REPORT['cgroup_layout'] = CGROUP.layout()\n        dump(OUT / 'cgroup-layout.json', REPORT['cgroup_layout'])")
    expected = expected.replace("        REPORT['admission'] = {'boot_id':", "        REPORT['owner_cgroup_limits'] = CGROUP.observe(int(owner['MainPID']), OWNER, 1073741824, 128)\n        REPORT['admission'] = {'boot_id':")
    expected = expected.replace("    entry = {'identity': identity, 'properties': p, 'listener_inode': inode}",
        "    entry = {'identity': identity, 'properties': p, 'listener_inode': inode}\n    entry['kernel_limits'] = CGROUP.observe(pid, UNIT, 536870912, 64)")
    expected = expected.replace('def cgroup_members(group):\n', 'def cgroup_members(group):\n    CGROUP.layout()  # A vanished/replaced hierarchy is not an empty owned group.\n')
    expected = expected.replace('MemoryMax=512M\nTasksMax=64',
        'ExecStartPre=/usr/bin/python3 -I -S -B {PACKET}/cgroup_guard.py --service-receipts {OUT}\nMemoryMax=512M\nTasksMax=64')
    assert (HERE/'run.py').read_text() == expected, 'driver changed beyond explicit additional guards'
    parsed = {str(p.relative_to(HERE)):ast.parse(p.read_bytes(),filename=str(p)) for p in HERE.rglob('*.py')}
    for name in ('owner.py','census.py','reference_native.py','bootstrap/sitecustomize.py','raofflineproxy.service','raofflineproxy-ctl','bindings.json'):
        assert (HERE/name).read_bytes() == (old/name).read_bytes(),name
    for name,digest in json.loads((HERE/'runner-seal.json').read_text()).items():
        assert sha((HERE/name).read_bytes())==digest,name
    for row in binding['evidence']:
        raw = (HERE/row['copy']).read_bytes()
        assert len(raw)==row['bytes'] and sha(raw)==row['sha256'],row['copy']
    config = (HERE/'cgroup-evidence/kernel-7.1.2.config').read_text().splitlines()
    assert all(line in config for line in ('# Linux/x86 7.1.2 Kernel Configuration','CONFIG_MEMCG=y',
        '# CONFIG_MEMCG_V1 is not set','CONFIG_CGROUP_PIDS=y'))
    mounts=(HERE/'cgroup-evidence/guest-mountinfo.txt').read_text()
    assert ' /sys/fs/cgroup/unified ' in mounts and ' - cgroup2 ' in mounts
    assert 'name=systemd' in mounts and not any(' - cgroup ' in l and 'memory' in l for l in mounts.splitlines())
    version=(HERE/'cgroup-evidence/guest-systemd-version.txt').read_text()
    assert '255.8' in version and 'default-hierarchy=hybrid' in version
    boot=binding['boot_config'];before=(HERE/'boot/syslinux.before.cfg').read_bytes();after=(HERE/'boot/syslinux.after.cfg').read_bytes()
    assert sha(before)==boot['before_sha256'] and sha(after)==boot['after_sha256']
    assert before.count(b'\n  APPEND ')==1 and b'cgroup' not in before
    assert after==before.rstrip(b'\n')+b' systemd.unified_cgroup_hierarchy=1\n'
    result=json.loads((HERE/'cgroup-evidence/attempt01-payload-result.json').read_text())
    assert result['status']=='FAIL' and result['commands']==[] and result['steps']==[]
    assert result['error']=='AssertionError: cgroup v2 required for this bounded packet'
    owner=json.loads((HERE/'cgroup-evidence/attempt01-owner-result.json').read_text())
    assert owner['original_child_exit']==1 and owner['remaining_children']==[] and owner['cleanup_errors']==[]
    assert (HERE/'cgroup-evidence/attempt01-original.rc').read_text().strip()=='1'
    assert (HERE/'cgroup-evidence/attempt01-cleanup-intervention.rc').read_text().strip()=='0'
    # Additional admission reads kernel state, never mutates limits or invokes a service.
    calls=[n for n in ast.walk(parsed['cgroup_guard.py']) if isinstance(n,ast.Call)]
    assert not any(isinstance(n.func,ast.Attribute) and n.func.attr in
                   ('setrlimit','kill','killpg','system','Popen','run') for n in calls)
    print(json.dumps({'status':'STATIC_ONLY_PASS','python_ast':sorted(parsed),'unchanged_original_files':copied,
        'original_manifest_sha256':binding['parent_manifest_sha256'],'exact_prospective_boot_text':boot,
        'kernel_configuration':'retained compiled 7.1.2: MEMCG=y, MEMCG_V1 disabled, CGROUP_PIDS=y',
        'observed_guest':'systemd255.8 hybrid; v2 under unified; no memory v1 mount',
        'old_cgroup_prerequisite_retained':True,'only_driver_changes':'additional layout/platform/enforced-kernel-limit checks and pre-start guard',
        'original_timers_lifecycle_worker_award_and_network_guards_unchanged':True,
        'owner_memory_bytes':1073741824,'owner_explicit_tasks_new':128,'service_memory_bytes':536870912,'service_tasks':64,
        'original_failure_preserved':True,'runtime':'UNRUN','fixture_imported_or_executed':False,
        'boot_or_vm_or_service_or_product_changed':False,'native_accepted_proof_replayed':False},indent=2))


if __name__=='__main__':
    main()
