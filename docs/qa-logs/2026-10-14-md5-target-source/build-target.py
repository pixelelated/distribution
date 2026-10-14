#!/usr/bin/env python3
"""UNRUN. Inside the newly admitted offline container only; no target execution."""
import hashlib
import json
import os
from pathlib import Path
import resource
import shlex
import shutil
import subprocess
import time

ROOT = Path('/work')
PACKET = Path('/packet')
BINDING = json.loads((PACKET / 'input-bindings.json').read_text())
TC = Path(BINDING['toolchain']['required_container_root'])
SEALED = ROOT / 'sources/fixture/docs/qa-logs/2026-10-13-rvz-regression-source'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def run(label, argv, env, stages, seconds=360):
    started = time.monotonic()
    argv = [str(x) for x in argv]
    write(ROOT / 'records' / (label + '-command.json'), argv)
    print('START ' + label, flush=True)
    with (ROOT / 'logs' / (label + '.stdout')).open('xb') as out, (ROOT / 'logs' / (label + '.stderr')).open('xb') as err:
        process = subprocess.Popen(argv, cwd=ROOT, env=env, stdout=out, stderr=err)
        timed_out = False
        try:
            code = process.wait(timeout=seconds)
        except subprocess.TimeoutExpired:
            # The outer owner stops this entire private container, including
            # compiler descendants; do not continue after a stage deadline.
            timed_out = True
            process.kill()
            code = process.wait(timeout=5)
    stages.append({'label':label, 'original_exit':code, 'timed_out':timed_out,
                   'elapsed':time.monotonic()-started})
    write(ROOT / 'records/stages.json', stages)
    if code != 0 or timed_out:
        raise RuntimeError('failed compile stage: ' + label)


def features(entry):
    words = shlex.split(entry['command'])
    return {word for word in words if word.startswith(('-I', '-D'))}


def contract(build, mode):
    database = json.loads((build / 'compile_commands.json').read_text())
    checks = []
    for product, consumer in (('libretro-common/src/utils/md5.c','md5-alignment.c'), ('hash_disc.c','wii-partition-probe.c')):
        prod = [e for e in database if e['file'].endswith('/' + product)]
        uses = [e for e in database if Path(e['file']).name == consumer]
        if len(prod) != 1 or len(uses) != 1:
            raise RuntimeError('ambiguous MD5/direct-source compile contract')
        checks.append({'product':product,'consumer':consumer,'missing':sorted(features(prod[0])-features(uses[0]))})
    bad = []
    for entry in database:
        words = shlex.split(entry['command'])
        required = {'-fsanitize=address,undefined','-fno-sanitize-recover=all','-fno-omit-frame-pointer','-g'}
        if not required <= set(words) or any(w.startswith('-fno-sanitize=') for w in words):
            bad.append(entry['file'])
    flags = [e for e in database if Path(e['file']).name in ('hash_disc.c','wii-partition-probe.c','md5.c','md5-alignment.c')]
    rvz_ok = all(('-DHAVE_RVZ_HASH' in features(e)) == (mode == 'candidate') for e in flags)
    report = {'direct_source_contracts':checks,'uninstrumented_or_disabled':bad,'rvz_feature_contract':rvz_ok,
              'translation_units':len(database),'status':'PASS' if not bad and rvz_ok and all(not c['missing'] for c in checks) else 'FAIL'}
    write(ROOT / 'records' / ('contract-' + mode + '.json'), report)
    shutil.copyfile(build / 'compile_commands.json', ROOT / 'records' / ('compile_commands-' + mode + '.json'))
    if report['status'] != 'PASS':
        raise RuntimeError('evaluated compiler contract failed; no build allowed')


def main():
    env = dict(os.environ, TMPDIR='/work/tmp', CCACHE_DISABLE='1', CCACHE_DIR='/work/tmp/ccache',
               PATH=str(TC / 'bin') + ':' + os.environ['PATH'])
    result = {'status':'FAIL','stages':[],'started':time.time(),'input_binding_sha256':sha(PACKET / 'input-bindings.json'),
              'candidate_commit':BINDING['candidate']['commit'],'baseline_repair':BINDING['baseline_repair']}
    try:
        for mode in ('baseline-repaired','candidate'):
            build = ROOT / 'builds' / mode
            source = ROOT / 'sources' / mode
            run('configure-' + mode, [TC / 'bin/cmake','-S',PACKET,'-B',build,'-G','Ninja',
                '-DCMAKE_TOOLCHAIN_FILE=' + str(TC / 'etc/cmake-x86_64-rocknix-linux-gnu.conf'),
                '-DES_SOURCE=' + str(source), '-DSEALED_PACKET=' + str(SEALED),
                '-DMD5_CONTROL_SOURCE=/work/sources/candidate/tests/md5-alignment.c',
                '-DENABLE_RVZ_HASH=' + ('ON' if mode == 'candidate' else 'OFF'),
                '-DCMAKE_EXPORT_COMPILE_COMMANDS=ON'],env,result['stages'],60)
            contract(build, mode)
            for source_name, suffix in (('build.ninja','build.ninja'), ('CMakeFiles/rules.ninja','rules.ninja'), ('CMakeCache.txt','CMakeCache.txt')):
                shutil.copyfile(build / source_name, ROOT / 'records' / (mode + '-' + suffix))
            targets = ['pix574-md5-alignment','pix574-regression-hash','pix574-wii-partition-probe']
            if mode == 'candidate': targets.append('pix574-fixture-writer')
            run('compile-' + mode,[TC / 'bin/cmake','--build',build,'--parallel','1','--target',*targets],env,result['stages'])
            dest = ROOT / 'artifacts' / mode
            dest.mkdir()
            for target in targets:
                product = build / target if target == 'pix574-md5-alignment' else build / 'controls/wii-controls/sealed-controls' / target
                shutil.copyfile(product, dest / target)
                (dest / target).chmod(0o755)
        dest = ROOT / 'artifacts/lib'
        dest.mkdir()
        for soname, item in BINDING['sanitizer_runtimes'].items():
            source = TC / item['relative']
            if sha(source) != item['sha256']: raise RuntimeError('sanitizer runtime identity changed')
            shutil.copyfile(source, dest / soname)
        result['artifacts'] = {str(p.relative_to(ROOT)):sha(p) for p in (ROOT / 'artifacts').rglob('*') if p.is_file()}
        result['contract_reports'] = {str(p.relative_to(ROOT)):sha(p) for p in (ROOT / 'records').glob('contract-*.json')}
        result['status'] = 'PASS'
    finally:
        result['ended'] = time.time()
        result['max_child_rss_kib'] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        for key in ('memory.peak','memory.events'):
            path = Path('/sys/fs/cgroup') / key
            result[key] = path.read_text() if path.exists() else None
        events = dict(line.split() for line in (result.get('memory.events') or '').splitlines())
        if not result.get('memory.peak') or not {'oom','oom_kill'} <= events.keys() or any(int(events[k]) != 0 for k in ('oom','oom_kill')):
            result['status'] = 'FAIL'
            result['resource_error'] = 'missing cgroup memory evidence or nonzero OOM events'
        write(ROOT / 'compile-result.json', result)
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__': raise SystemExit(main())
