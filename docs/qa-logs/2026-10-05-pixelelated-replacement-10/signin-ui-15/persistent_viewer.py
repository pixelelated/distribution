"""Read-only persistent RFB observer; screenshots remain separate acceptance proof.

Refs #449. No input, resize or credentials. A complete frame does not establish
that the displayed page is current. See RFC6143 sections 7.5.3 and 7.6.1.
"""
import datetime
import hashlib
import json
import socket
import struct
import time


class ObserverStopped(Exception):
    pass


def observe_frames(host, port, out, stop, ready, errors, timeout=5.0):
    sock = None
    phase = 'connect'
    deadline = time.monotonic() + timeout
    index = 0

    def event(kind, **values):
        values.update(kind=kind, utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      monotonic=time.monotonic(), phase=phase)
        with (out / 'observer-events.jsonl').open('a') as f:
            f.write(json.dumps(values) + '\n')

    def read(count):
        data = bytearray()
        while len(data) < count:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(f'{phase}: {len(data)}/{count} bytes')
            sock.settimeout(remaining)
            part = sock.recv(count - len(data))
            if not part:
                raise OSError(f'{phase}: EOF at {len(data)}/{count} bytes')
            data.extend(part)
        return bytes(data)

    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        phase = 'handshake'
        if read(12) != b'RFB 003.008\n':
            raise OSError('RFB 3.8 required')
        sock.sendall(b'RFB 003.008\n')
        count = read(1)[0]
        if not count or 1 not in read(count):
            raise OSError('unauthenticated loopback RFB required')
        sock.sendall(b'\x01')
        if struct.unpack('>I', read(4))[0]:
            raise OSError('RFB security refused')
        sock.sendall(b'\x01')
        width, height = struct.unpack('>HH', read(4))
        if (width, height) != (640, 480):
            raise OSError('unexpected panel size')
        read(16)
        name_size = struct.unpack('>I', read(4))[0]
        if name_size > 4096:
            raise OSError('oversized server name')
        read(name_size)
        sock.sendall(b'\0\0\0\0' + struct.pack('>BBBBHHHBBB', 32, 24, 0, 1,
                     255, 255, 255, 16, 8, 0) + b'\0\0\0')
        sock.sendall(b'\x02\0' + struct.pack('>Hi', 1, 0))
        while not stop.is_set():
            phase = 'frame-boundary'
            sock.sendall(b'\x03\0' + struct.pack('>HHHH', 0, 0, width, height))
            deadline = time.monotonic() + timeout
            # Only an established observer may wait quietly at a message boundary.
            # A partial message, incomplete frame or missing initial frame stays bounded.
            if index:
                idle_recorded = False
                while True:
                    if stop.is_set():
                        raise ObserverStopped()
                    sock.settimeout(min(timeout, 0.2))
                    try:
                        first = sock.recv(1)
                    except socket.timeout:
                        if not idle_recorded:
                            event('idle-after-complete-frame', complete_frames=index)
                            idle_recorded = True
                        continue
                    if not first:
                        raise OSError('frame-boundary: EOF')
                    break
                deadline = time.monotonic() + timeout
            else:
                first = read(1)
            phase = 'frame-message'
            framebuffer = bytearray(width * height * 4)
            coverage = bytearray(width * height)
            covered = 0
            while covered < width * height:
                message = first[0]
                if message == 2:
                    first = read(1)
                    continue
                if message == 3:
                    read(3)
                    size = struct.unpack('>I', read(4))[0]
                    if size > 1048576:
                        raise OSError('oversized clipboard message')
                    read(size)  # discard; never retain clipboard content
                    first = read(1)
                    continue
                if message != 0:
                    raise OSError(f'unsupported RFB message {message}')
                read(1)
                rectangles = struct.unpack('>H', read(2))[0]
                for _ in range(rectangles):
                    x, y, rw, rh, encoding = struct.unpack('>HHHHi', read(12))
                    if encoding != 0 or not rw or not rh or x + rw > width or y + rh > height:
                        raise OSError('invalid raw rectangle')
                    pixels = read(rw * rh * 4)
                    for row in range(rh):
                        at = (y + row) * width + x
                        framebuffer[at * 4:(at + rw) * 4] = pixels[row * rw * 4:(row + 1) * rw * 4]
                        covered += rw - sum(coverage[at:at + rw])
                        coverage[at:at + rw] = b'\x01' * rw
                if covered < width * height:
                    first = read(1)
            rgb = bytearray(width * height * 3)
            rgb[0::3], rgb[1::3], rgb[2::3] = framebuffer[2::4], framebuffer[1::4], framebuffer[0::4]
            record = {'frame': f'viewer-{index:04d}.png', 'monotonic': time.monotonic(),
                      'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      'rgb_sha256': hashlib.sha256(rgb).hexdigest()}
            with (out / 'viewer-frames.jsonl').open('a') as f:
                f.write(json.dumps(record) + '\n')
            index += 1
            ready.set()
            stop.wait(.1)
        event('stopped', complete_frames=index)
    except ObserverStopped:
        event('stopped-at-idle-boundary', complete_frames=index)
    except Exception as exc:
        errors.append(type(exc).__name__ + ': ' + str(exc))
        event('error', error=errors[-1], complete_frames=index)
        ready.set()
    finally:
        if sock is not None:
            sock.close()
