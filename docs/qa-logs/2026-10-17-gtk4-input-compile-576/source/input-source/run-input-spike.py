#!/usr/bin/env python3
"""UNRUN: native-input fixture, disposable QEMU guest only; no real providers."""
import argparse
import hashlib
import importlib.util
import os
from pathlib import Path
import selectors
import signal
import socket
import struct
import subprocess
import time


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--binary', type=Path, required=True)
    ap.add_argument('--binary-sha256', required=True)
    ap.add_argument('--seconds', type=int, default=90, choices=range(10, 121))
    args = ap.parse_args()
    # This guard excludes the handheld and ordinary host. A coordinator-owned
    # VM supervisor still owns pressure, teardown, result delivery and admission.
    product = Path('/sys/class/dmi/id/product_name').read_text().strip()
    if not any(x in product.lower() for x in ('qemu', 'kvm', 'standard pc')):
        raise SystemExit('refusing: disposable QEMU guest required')
    binary = args.binary.resolve(strict=True)
    if hashlib.sha256(binary.read_bytes()).hexdigest() != args.binary_sha256:
        raise SystemExit('binary hash mismatch')
    root = Path(__file__).resolve().parent
    import json
    receipt = json.loads((root / 'preparation.json').read_text())
    native = root / 'native_keyboard.py'
    if hashlib.sha256(native.read_bytes()).hexdigest() != receipt['files']['native_keyboard.py']:
        raise SystemExit('native input source mismatch')
    spec = importlib.util.spec_from_file_location('native_keyboard_fixture', native)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    keyboard = module.RemoteKeyboard()
    parent, child = socket.socketpair(socket.AF_UNIX, socket.SOCK_SEQPACKET)
    proc = None
    selector = selectors.DefaultSelector()
    try:
        if not keyboard.open():
            raise RuntimeError('native input device unavailable')
        env = os.environ.copy()
        env['PIX_GTK4_INPUT_FD'] = str(child.fileno())
        env.pop('CLOUD_SIGNIN_DEBUG', None)
        proc = subprocess.Popen([str(binary)], env=env, pass_fds=(child.fileno(),), start_new_session=True)
        child.close()
        selector.register(parent, selectors.EVENT_READ)
        deadline = time.monotonic() + args.seconds
        delivered = 0
        while proc.poll() is None:
            if time.monotonic() >= deadline:
                raise TimeoutError('bounded fixture deadline')
            for key, _ in selector.select(0.1):
                packet = key.fileobj.recv(8)
                if not packet:
                    proc.wait(timeout=2)
                    break
                if len(packet) != 4:
                    raise RuntimeError('invalid input request length')
                value, = struct.unpack('!I', packet)
                names = {0xff08: 'backspace', 0xff09: 'tab', 0xff0d: 'enter'}
                if 32 <= value <= 126:
                    success = keyboard.type_text(chr(value)) == 1
                elif value in names:
                    success = keyboard.press(names[value])
                else:
                    success = False
                parent.sendall(bytes([int(success)]))
                if not success:
                    raise RuntimeError('native input request rejected')
                delivered += 1
        result = proc.wait(timeout=2)
        print('fixture exit=%d emitted=%d; DOM/native frames are separate acceptance' % (result, delivered))
        return result
    finally:
        selector.close()
        parent.close()
        child.close()
        keyboard.close()
        if proc is not None and proc.poll() is None:
            # Only signal a still-owned direct child group. If the parent has
            # already exited, the outer VM supervisor owns any descendants.
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait(timeout=2)


if __name__ == '__main__':
    raise SystemExit(main())
