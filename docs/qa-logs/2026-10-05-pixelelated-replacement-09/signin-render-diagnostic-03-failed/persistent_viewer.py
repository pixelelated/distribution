import socket,struct,time,json,hashlib,datetime
from PIL import Image
def observe_frames(host, port, out, stop, ready, errors, timeout=5.0):
    """One frame from a VNC server as (width, height, RGB bytes): RFB 3.8,
    no security (QEMU's -vnc on loopback has none), raw encoding, one
    non-incremental update. The standard library only, like the rest of this
    file. This is the frame source under a GL scanout (fork #291)."""
    def read(n):
        b = b""
        while len(b) < n:
            c = s.recv(n - len(b))
            if not c:
                raise OSError("vnc closed")
            b += c
        return b
    s = socket.create_connection((host, port), timeout=timeout)
    try:
        read(12)
        s.sendall(b"RFB 003.008\n")
        n = read(1)[0]
        if n == 0:
            rl = struct.unpack(">I", read(4))[0]
            raise OSError("vnc refused: " + read(rl).decode("utf-8", "replace"))
        if 1 not in read(n):
            raise OSError("vnc wants a security type this grabber does not speak")
        s.sendall(b"\x01")
        if struct.unpack(">I", read(4))[0] != 0:
            raise OSError("vnc security failed")
        s.sendall(b"\x01")
        w, h = struct.unpack(">HH", read(4))
        read(16)
        read(struct.unpack(">I", read(4))[0])
        # 32-bit true colour, little-endian, so a raw pixel is B G R x
        s.sendall(b"\x00\x00\x00\x00" + struct.pack(">BBBBHHHBBB", 32, 24, 0, 1, 255, 255, 255, 16, 8, 0) + b"\x00\x00\x00")
        s.sendall(b"\x02\x00" + struct.pack(">H", 1) + struct.pack(">i", 0))
        index=0
        while not stop.is_set():
            s.sendall(b"\x03\x00" + struct.pack(">HHHH", 0, 0, w, h))
            fb = bytearray(w * h * 4)
            covered = 0
            deadline = time.time() + timeout
            while covered < w * h and time.time() < deadline:
                mt = read(1)[0]
                if mt == 2:
                    continue
                if mt == 3:
                    read(3)
                    read(struct.unpack(">I", read(4))[0])
                    continue
                if mt != 0:
                    raise OSError("vnc message %d" % mt)
                read(1)
                for _ in range(struct.unpack(">H", read(2))[0]):
                    x, y, rw, rh, enc = struct.unpack(">HHHHi", read(12))
                    if enc != 0:
                        raise OSError("vnc encoding %d" % enc)
                    data = read(rw * rh * 4)
                    for row in range(rh):
                        o = ((y + row) * w + x) * 4
                        fb[o:o + rw * 4] = data[row * rw * 4:(row + 1) * rw * 4]
                    covered += rw * rh
            if covered < w*h:raise OSError('incomplete persistent frame')
            if (w,h)!=(640,480):raise OSError('unexpected panel size')
            rgb=bytearray(w*h*3);rgb[0::3]=fb[2::4];rgb[1::3]=fb[1::4];rgb[2::3]=fb[0::4]
            name=f'viewer-{index:04d}.png';Image.frombytes('RGB',(w,h),bytes(rgb)).save(out/name)
            record={'frame':name,'monotonic':time.monotonic(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rgb_sha256':hashlib.sha256(rgb).hexdigest()}
            with (out/'viewer-frames.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
            index+=1;ready.set();stop.wait(.1)
    except Exception as exc:
        errors.append(type(exc).__name__+': '+str(exc))
        ready.set()
    finally:
        s.close()
