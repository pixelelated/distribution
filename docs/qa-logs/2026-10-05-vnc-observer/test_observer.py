"""Real loopback protocol controls for #449; no guest or provider involved."""
from pathlib import Path
import hashlib
import json
import runpy
import socket
import struct
import tempfile
import threading
import time

observe = runpy.run_path(str(Path(__file__).with_name('persistent_viewer.py')))['observe_frames']
pixel = b'\x11\x22\x33\0'
expected = hashlib.sha256(b'\x33\x22\x11' * (640 * 480)).hexdigest()


def rectangle(x=0, y=0, width=640, height=480, encoding=0):
    return struct.pack('>HHHHi', x, y, width, height, encoding) + pixel * (width * height)


def case(name, should_pass, server_action):
    stop, ready, server_done = threading.Event(), threading.Event(), threading.Event()
    errors, server_errors = [], []
    with tempfile.TemporaryDirectory(prefix='pixelelated-vnc-control-') as temporary:
        out = Path(temporary)
        with socket.socket() as listener:
            listener.bind(('127.0.0.1', 0))
            listener.listen(1)

            def server():
                try:
                    with listener.accept()[0] as connection:
                        connection.settimeout(3)

                        def read(n):
                            data = b''
                            while len(data) < n:
                                part = connection.recv(n - len(data))
                                assert part, 'client disconnected unexpectedly'
                                data += part
                            return data

                        connection.sendall(b'RFB 003.008\n')
                        assert read(12) == b'RFB 003.008\n'
                        connection.sendall(b'\x01\x01')
                        assert read(1) == b'\x01'
                        connection.sendall(b'\0' * 4)
                        assert read(1) == b'\x01'
                        connection.sendall(struct.pack('>HH', 640, 480) + b'\0' * 20)
                        assert read(20)[0] == 0
                        assert read(8) == b'\x02\0\0\x01\0\0\0\0'
                        assert read(10) == b'\x03\0' + struct.pack('>HHHH', 0, 0, 640, 480)
                        server_action(connection, read, stop)
                except Exception as exc:
                    server_errors.append(repr(exc))
                finally:
                    server_done.set()

            thread = threading.Thread(target=server)
            thread.start()
            client = threading.Thread(target=observe, args=('127.0.0.1', listener.getsockname()[1], out, stop, ready, errors, .5))
            client.start()
            client.join(4)
            assert not client.is_alive(), name + ': observer exceeded bound'
            stop.set()
            thread.join(3)
            assert server_done.is_set() and not server_errors, (name, server_errors)
            assert bool(errors) != should_pass, (name, errors)
            frames = [json.loads(s) for s in (out / 'viewer-frames.jsonl').read_text().splitlines()] if (out / 'viewer-frames.jsonl').exists() else []
            if should_pass:
                assert frames and all(frame['rgb_sha256'] == expected for frame in frames)
            else:
                events = [json.loads(s) for s in (out / 'observer-events.jsonl').read_text().splitlines()]
                assert events[-1]['kind'] == 'error' and events[-1]['phase']
            print('PASS', name, 'complete_frames=' + str(len(frames)), flush=True)


def idle(connection, read, stop):
    connection.sendall(b'\0\0\0\x01' + rectangle())
    read(10)
    time.sleep(1.1)  # more than twice the read timeout, after a complete frame
    stop.set()
    time.sleep(.25)


def fragmented(connection, read, stop):
    data = b'\0\0\0\x02' + rectangle(width=320) + rectangle(x=320, width=320)
    for at in [0, 1, 3, 7, 12, 39]:
        end = {0: 1, 1: 3, 3: 7, 7: 12, 12: 39, 39: len(data)}[at]
        connection.sendall(data[at:end])
        time.sleep(.01)
    read(10)
    stop.set()
    time.sleep(.25)


def partial(data):
    def send(connection, read, stop):
        connection.sendall(data)
        time.sleep(.8)
    return send


case('complete-frame then idle then clean stop', True, idle)
case('fragmented headers/pixels and distinct rectangles', True, fragmented)
case('initial frame never arrives', False, partial(b''))
case('truncated frame header', False, partial(b'\0\0\0'))
case('truncated pixel payload', False, partial(b'\0\0\0\x01' + rectangle()[:30]))
case('overlapping area cannot masquerade as full coverage', False,
     partial(b'\0\0\0\x02' + rectangle(width=320) + rectangle(width=320)))
case('out-of-panel rectangle', False,
     partial(b'\0\0\0\x01' + struct.pack('>HHHHi', 640, 0, 1, 1, 0)))
case('unsupported encoding', False,
     partial(b'\0\0\0\x01' + struct.pack('>HHHHi', 0, 0, 1, 1, 5)))
case('EOF after a complete frame', False,
     lambda connection, read, stop: (connection.sendall(b'\0\0\0\x01' + rectangle()), read(10)))
print('PASS all nine persistent-observer protocol controls')
