#!/usr/bin/env python3
"""UNRUN. Synthetic recovery refusal controls; no Docker or target calls."""
import argparse
import copy
import json
from pathlib import Path
import runpy
import tempfile

HERE = Path(__file__).resolve().parent
R = runpy.run_path(str(HERE / 'recovery.py'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True, help='new prepared recovery export')
    args = parser.parse_args()
    R['validate_export'](args.input)
    known = R['packet']()
    cid = known['cid']
    checks = []
    for label, code, out, err, identity, expected in [
        ('original-lowercase',1,'\n','error: no such object: '+cid+'\n',cid,True),
        ('old-capitalization',1,'','Error: No such object: '+cid,cid,True),
        ('typed-container',1,'\n','Error response from daemon: No such container: '+cid+'\n',cid,True),
        ('bare-diagnostic',1,'','No such object: '+cid,cid,True),
        ('daemon-down',1,'','Cannot connect to the Docker daemon: '+cid,cid,False),
        ('permission',1,'','permission denied: '+cid,cid,False),
        ('wrong-id',1,'','error: no such object: '+'a'*64,cid,False),
        ('short-id',1,'','error: no such object: '+cid[:12],cid,False),
        ('id-suffix',1,'','error: no such object: '+cid+'0',cid,False),
        ('extra-error',1,'','error: no such object: '+cid+'\ndaemon failed',cid,False),
        ('echo-substring',1,'','failed querying "error: no such object: '+cid+'"',cid,False),
        ('error-exit2',2,'','error: no such object: '+cid,cid,False),
        ('success-exit',0,'','error: no such object: '+cid,cid,False),
        ('live-stdout',1,'true\n','error: no such object: '+cid,cid,False),
        ('stopped-stdout',1,'false\n','error: no such object: '+cid,cid,False),
        ('malformed-id',1,'','error: no such object: '+cid[:12],cid[:12],False),
    ]:
        assert R['absent'](code,out,err,identity) is expected, label
        checks.append(label)
    records = {name:json.loads((args.input/name).read_text()) for name in known['evidence'] if name.endswith('.json')}
    binding = json.loads((args.input/'packet/input-bindings.json').read_text())
    R['validate_records'](records,binding,known)
    checks.append('exact-known-records')
    changes = [
        ('forced-stop',['result.json','forced_container_stop_exit'],0),
        ('outer-other-error',['result.json','container_cleanup_error'],'other error'),
        ('outer-timeout',['result.json','timed_out'],True),
        ('docker-exit',['result.json','original_docker_exit'],1),
        ('sampler-error',['result.json','sampling','error'],'failed'),
        ('inner-failure',['compile-result.json','status'],'FAIL'),
        ('stage-failure',['compile-result.json','stages',1,'original_exit'],1),
        ('stage-timeout',['compile-result.json','stages',2,'timed_out'],True),
        ('missing-stage',['compile-result.json','stages'],records['compile-result.json']['stages'][:3]),
        ('different-source',['compile-result.json','candidate_commit'],'a'*40),
        ('different-artifact',['compile-result.json','artifacts'],{}),
        ('oom',['compile-result.json','memory.events'],'oom 1\noom_kill 0\n'),
        ('missing-oom',['compile-result.json','memory.events'],'high 0\n'),
        ('forced-resource-failure',['compile-result.json','resource_error'],'failed'),
        ('contract-failed',['records/contract-candidate.json','status'],'FAIL'),
        ('sanitizer-disabled',['records/contract-candidate.json','uninstrumented_or_disabled'],['md5.c']),
        ('inspect-daemon-error',['container-absence-readback.json','checks',0,'stderr'],'daemon unavailable'),
        ('inventory-failure',['container-absence-readback.json','checks',1,'original_exit'],1),
        ('inventory-present',['container-absence-readback.json','checks',1,'stdout'],cid+'\n'),
        ('inventory-malformed',['container-absence-readback.json','checks',1,'stdout'],'not-an-id\n'),
        ('pre-failure-proof',['container-absence-readback.json','utc'],'2026-10-14T00:00:00+00:00'),
        ('host-exits-missing',['container-absence-readback.json','host_pids_absent'],[]),
        ('launcher-relabelled',['submit/launcher-result.json','runner_returncode'],0),
    ]
    for label, path, value in changes:
        changed = copy.deepcopy(records)
        target = changed
        for key in path[:-1]: target = target[key]
        target[path[-1]] = value
        try:
            R['validate_records'](changed,binding,known)
        except (RuntimeError, KeyError, ValueError):
            checks.append(label)
        else:
            raise AssertionError('accepted '+label)
    with tempfile.TemporaryDirectory(prefix='pix574-recovery-controls-') as temp:
        root = Path(temp)
        (root/'member').write_bytes(b'synthetic')
        hashes = {'member':R['sha'](root/'member')}
        R['verify'](root,hashes)
        checks.append('matching-hash')
        (root/'member').write_bytes(b'changed')
        try: R['verify'](root,hashes)
        except RuntimeError: checks.append('changed-hash')
        else: raise AssertionError('changed hash accepted')
        (root/'member').unlink()
        try: R['verify'](root,hashes)
        except RuntimeError: checks.append('missing-member')
        else: raise AssertionError('missing member accepted')
    print(json.dumps({'status':'PASS','count':len(checks),'checks':checks}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
