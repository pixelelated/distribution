#!/usr/bin/env python3
"""UNRUN. One serial/monitor operation at a time; never SSH or automatic replay.

capture saves a 640x480 PPM; advance requires explicit reviewed-frame text before
one x press (entry/error only). next consumes an already completed case. Original
serial wrapper, guest command and monitor exits are saved independently.
"""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import signal
import subprocess
import sys
import time
import uuid

GUEST = '/tmp/pix-input/dolphin/batch/guest-batch.py'
HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, data):
    Path(path).write_text(json.dumps(data, indent=2) + '\n')


def execute(args, directory, argv, timeout=35):
    number = uuid.uuid4().hex[:12]
    prefix = directory / number
    timed_out = False
    with prefix.with_suffix('.stdout').open('wb') as stdout, prefix.with_suffix('.stderr').open('wb') as stderr:
        process = subprocess.Popen(argv, stdout=stdout, stderr=stderr, start_new_session=True)
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGKILL)
            code = process.wait(timeout=5)
    save(prefix.with_suffix('.json'), {'argv':argv, 'original_exit':code, 'timed_out':timed_out})
    require(code == 0 and not timed_out, 'original host tool exit failed; see ' + str(prefix))
    return prefix.with_suffix('.stdout').read_text(errors='replace')


def serial(args, directory, *words):
    tag = 'PIX581_EXIT_' + uuid.uuid4().hex
    command = shlex.join(['/usr/bin/python3', '-I', '-S', '-B', GUEST, *words])
    # vm-serial's 0 means END was received, not that the guest command succeeded.
    command += "; pix581_rc=$?; printf '\\n" + tag + "=%s\\n' \"$pix581_rc\""
    output = execute(args, directory, [str(args.repo / 'tools/vm-serial'), '--socket', args.serial,
                     '--timeout', '15', 'sh', command], timeout=22)
    codes = re.findall(r'^' + tag + r'=([0-9]+)\r?$', output, re.M)
    require(codes == ['0'], 'guest command failed or its original exit marker is absent')
    messages = re.findall(r'^PIX581_JSON=(.*)\r?$', output, re.M)
    require(len(messages) == 1, 'missing/ambiguous guest JSON response')
    return json.loads(messages[0])


def visual(args, directory, *words):
    return execute(args, directory, [str(args.repo / 'tools/vm-visual-qa'), '--monitor', args.monitor, *words], timeout=25)


def ppm_size(path):
    # Header only. vm-visual-qa writes raw P6 without requiring PNG conversion.
    with path.open('rb') as stream:
        tokens = []
        while len(tokens) < 4:
            line = stream.readline(256)
            require(line and len(line) < 256, 'malformed PPM header')
            tokens.extend(line.split(b'#', 1)[0].split())
        require(tokens[0] == b'P6' and tokens[3] == b'255', 'unsupported PPM')
        width, height = int(tokens[1]), int(tokens[2])
        require(path.stat().st_size - stream.tell() == width * height * 3, 'truncated/extra PPM pixels')
        return [width, height]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('start', 'status', 'capture', 'advance', 'next', 'abort'))
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--serial', required=True)
    parser.add_argument('--monitor', required=True)
    parser.add_argument('--receipts', type=Path, required=True)
    parser.add_argument('--review', help='your actual frame review or consumed-exit note; never a generated PASS')
    args = parser.parse_args()
    args.receipts.mkdir(parents=True, exist_ok=True)
    with (args.receipts / 'host.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        binding = json.loads((HERE / 'binding.json').read_text())
        for name, digest in binding['host_tools'].items():
            require(sha(args.repo / name) == digest, 'host tool changed: ' + name)
        invocation = args.receipts / (time.strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:8])
        invocation.mkdir()
        if args.operation in ('start', 'abort'):
            words = ['start', '--disposable-vm'] if args.operation == 'start' else ['abort']
            print(json.dumps(serial(args, invocation, *words), indent=2))
            return 0
        state = serial(args, invocation, 'status')
        save(invocation / 'status.json', state)
        if args.operation == 'status':
            print(json.dumps(state, indent=2))
            return 0
        phase, token = state['phase'], state['token']
        require(re.fullmatch('[0-9]{2}-(entry|error|returned|complete)', token), 'not an actionable stage')
        capture = args.receipts / (token + '-capture.json')
        action = args.receipts / (token + '-action.json')
        if args.operation == 'capture':
            require(phase in ('entry','error','returned'), 'no frame due at this stage')
            require(not action.exists(), 'stage already advanced; never replay')
            visual(args, invocation, 'settle', '--timeout', '12')
            frame = invocation / (state['case']['id'] + '-' + phase + '.ppm')
            visual(args, invocation, 'shot', str(frame.resolve()))
            require(ppm_size(frame) == [640,480], 'frame is not 640x480; no advance')
            require(serial(args, invocation, 'status')['token'] == token, 'stage changed while capturing')
            save(capture, {'token':token, 'frame':str(frame.resolve()), 'sha256':sha(frame), 'size':[640,480]})
            print(str(frame.resolve()))
            return 0
        require(args.review and 1 <= len(args.review) <= 1000, 'explicit review note required')
        if args.operation == 'next':
            require(phase == 'complete', 'next only consumes a completed case')
        else:
            require(phase in ('entry','error','returned'), 'use next for completed cases')
            receipt = json.loads(capture.read_text())
            require(receipt['token'] == token and sha(receipt['frame']) == receipt['sha256'], 'capture missing/changed')
        # Claim BEFORE input. If the monitor or serial response is lost, stop and
        # diagnose; never send x a second time. Abort remains available.
        with action.open('x') as stream:
            json.dump({'token':token, 'review':args.review, 'input_due':phase in ('entry','error'),
                       'status':'CLAIMED; consult command exits'}, stream, indent=2)
        if phase in ('entry','error'):
            visual(args, invocation, 'key', 'x')
        response = serial(args, invocation, 'advance', '--token', token, '--review', args.review)
        save(invocation / 'advanced.json', response)
        print(json.dumps(response))
        return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print('REFUSED: ' + str(exc), file=sys.stderr)
        sys.exit(1)
