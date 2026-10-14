#!/usr/bin/env python3
"""UNRUN. Coordinator's admitted compile entry; exports public source, never executes targets."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import threading
import time

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok: raise RuntimeError(message)


def sha(path):
    with path.open('rb') as stream: return hashlib.file_digest(stream, 'sha256').hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def git(repo, *words):
    return subprocess.check_output(['git','-C',str(repo),*words], timeout=30)


def export(repo, revision, files, root):
    total = 0
    for name, expected in files.items():
        relative = Path(name)
        require(not relative.is_absolute() and '..' not in relative.parts, 'unsafe source member')
        data = git(repo, 'show', revision + ':' + name)
        total += len(data)
        require(total <= 16 * 1024**2, 'source closure unexpectedly large')
        require(hashlib.sha256(data).hexdigest() == expected, 'source identity mismatch: ' + name)
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream: stream.write(data)


def verify(root, files):
    for name, expected in files.items():
        require(sha(root / name) == expected, 'staged source changed: ' + name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--owner', type=Path, required=True)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--es-repo', type=Path, required=True)
    args = parser.parse_args()
    owner = args.owner
    require(re.fullmatch(r'/workspace/tmp/[A-Za-z0-9_-]+',str(owner)), 'simple new owner name required')
    require(owner.is_absolute() and owner.resolve() == owner and owner.is_relative_to(Path('/workspace/tmp')) and owner.is_dir(), 'fresh real /workspace/tmp owner required')
    require(os.getuid() != 0, 'run the admitted build as the normal build user')
    require(os.environ.get('RASTERATOPS_BUILD_RUN'), 'invoke through admitted watch-build')
    require(not (owner / 'compile-result.json').exists(), 'owner already used')
    binding = json.loads((HERE / 'input-bindings.json').read_text())
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ',1)
        require(Path(name).name == name and sha(HERE / name) == digest, 'packet changed')
    require(git(args.es_repo,'rev-parse','HEAD').decode().strip() == binding['candidate']['commit'], 'candidate checkout is not frozen314da58d')
    require(not git(args.es_repo,'status','--porcelain').strip(), 'candidate checkout is dirty')
    for item in binding['toolchain']['files'].values():
        require(sha(Path(item['path'])) == item['sha256'], 'toolchain changed')
    for name in ('sources','builds','tmp','artifacts'):
        (owner / name).mkdir()  # exclusive: no old source/build/binary reuse
    for name in ('logs','records'):
        (owner / name).mkdir(exist_ok=True)
        require(not list((owner / name).iterdir()), 'compile log/record directory is not empty')
    with (owner / 'compile-started').open('x') as stream: stream.write(str(time.time()) + '\n')
    export(args.es_repo,binding['candidate']['commit'],binding['candidate']['files'],owner / 'sources/candidate')
    export(args.es_repo,binding['candidate']['commit'],{binding['md5_driver']['path']:binding['md5_driver']['sha256']},owner / 'sources/candidate')
    export(args.es_repo,binding['pristine_baseline']['commit'],binding['pristine_baseline']['files'],owner / 'sources/baseline-repaired')
    md5 = binding['baseline_repair']['path']
    repaired = owner / 'sources/baseline-repaired' / md5
    require(sha(repaired) == binding['baseline_repair']['before'], 'baseline is not pristine before its one-file repair')
    repaired.write_bytes((owner / 'sources/candidate' / md5).read_bytes())
    baseline_files = dict(binding['pristine_baseline']['files'], **{md5:binding['baseline_repair']['after']})
    verify(owner / 'sources/baseline-repaired',baseline_files)
    export(args.repo,binding['sealed_fixture']['commit'],binding['sealed_fixture']['files'],owner / 'sources/fixture')
    write(owner / 'records/source-composition.json', {'candidate':binding['candidate']['commit'],
        'pristine_baseline':binding['pristine_baseline']['commit'],'baseline_repair':binding['baseline_repair'],
        'input_binding_sha256':sha(HERE / 'input-bindings.json')})
    physical = Path(binding['toolchain']['physical_root']).parents[1]
    inside = Path(binding['toolchain']['required_container_root']).parents[1]
    # Only tiny new source snapshots and this owner are writable; accepted cache
    # retains the historical absolute prefix and is mounted read-only.
    name = 'pix574-md5-' + hashlib.sha256(str(owner).encode()).hexdigest()[:12]
    command = ['docker','run','--pull=never','--rm','--name',name,'--cidfile',str(owner / 'container.cid'),
        '--network','none','--read-only','--memory','4g','--memory-swap','4g','--cpus','2','--pids-limit','256',
        '--user',str(os.getuid()) + ':' + str(os.getgid()),
        '-v',str(physical) + ':' + str(inside) + ':ro','-v',str(HERE) + ':/packet:ro',
        '-v',str(owner) + ':/work:rw',binding['builder'],'python3','-I','-B','/packet/build-target.py']
    write(owner / 'records/docker-command.json',command)
    result = {'status':'FAIL','started':time.time(),'original_docker_exit':None,'timed_out':False}
    done = threading.Event()
    sampling = {'samples':0,'error':None}
    def sample():
        try:
            with (owner / 'host-resources.jsonl').open('x') as stream:
                while not done.is_set():
                    stat = os.statvfs(owner)
                    row = {'monotonic':time.monotonic(),'available_bytes':stat.f_bavail*stat.f_frsize,
                           'meminfo':Path('/proc/meminfo').read_text(),'pressure':Path('/proc/pressure/memory').read_text()}
                    stream.write(json.dumps(row)+'\n'); stream.flush()
                    sampling['samples'] += 1
                    done.wait(1)
        except Exception as exc:
            sampling['error'] = repr(exc)
    sampler = threading.Thread(target=sample)
    sampler.start()
    process = None
    def interrupt(_sig, _frame): raise KeyboardInterrupt('owned compile interrupted')
    signal.signal(signal.SIGTERM,interrupt)
    try:
        with (owner / 'logs/container.stdout').open('xb') as out, (owner / 'logs/container.stderr').open('xb') as err:
            process = subprocess.Popen(command,stdout=out,stderr=err)
            write(owner / 'records/docker-client.json',{'pid':process.pid})
            try:
                result['original_docker_exit'] = process.wait(timeout=900)
            except subprocess.TimeoutExpired:
                result['timed_out'] = True
                raise RuntimeError('900 second compile allocation expired')
        require(result['original_docker_exit'] == 0,'original container command failed')
        compiled = json.loads((owner / 'compile-result.json').read_text())
        require(compiled['status'] == 'PASS','inner compiler failure')
        verify(owner,compiled['artifacts'])
        verify(owner / 'sources/candidate',binding['candidate']['files'])
        verify(owner / 'sources/baseline-repaired',baseline_files)
        require(git(args.es_repo,'rev-parse','HEAD').decode().strip() == binding['candidate']['commit'] and not git(args.es_repo,'status','--porcelain').strip(),'source checkout changed')
        result['status'] = 'PASS'
    finally:
        try:
            retire_container(owner, result)
        except Exception as exc:
            result['container_cleanup_error'] = repr(exc)
            result['status'] = 'FAIL'
        finally:
            if process is not None and process.poll() is None:
                process.terminate()
                try: process.wait(timeout=10)
                except subprocess.TimeoutExpired: process.kill(); process.wait(timeout=5)
            if process is not None: result['original_docker_exit'] = process.returncode
            done.set(); sampler.join(timeout=5)
            result['sampler_exited'] = not sampler.is_alive()
            result['sampling'] = sampling
            if not result['sampler_exited'] or sampling['error'] or not sampling['samples']: result['status'] = 'FAIL'
            result['ended'] = time.time()
            write(owner / 'result.json',result)
    return 0 if result['status'] == 'PASS' else 1


def retire_container(owner, result):
    cidfile = owner / 'container.cid'
    if cidfile.exists():
        cid = cidfile.read_text().strip()
        require(re.fullmatch('[0-9a-f]{64}',cid),'invalid owned container ID')
        check = subprocess.run(['docker','inspect','--format','{{.State.Running}}',cid],capture_output=True,text=True,timeout=15)
        write(owner / 'records/container-final-inspect.json', {'original_exit':check.returncode,'stdout':check.stdout,'stderr':check.stderr})
        if check.returncode != 0:
            require('No such object' in check.stderr and cid in check.stderr, 'container absence is not established')
        else:
            require(check.stdout.strip() in ('true','false'), 'malformed container state')
        if check.returncode == 0 and check.stdout.strip() == 'true':
            stop = subprocess.run(['docker','stop','--time','10',cid],capture_output=True,text=True,timeout=25)
            result['forced_container_stop_exit'] = stop.returncode
            result['status'] = 'FAIL'


if __name__ == '__main__': raise SystemExit(main())
