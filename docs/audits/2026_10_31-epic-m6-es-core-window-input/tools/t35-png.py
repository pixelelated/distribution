"""A stdlib PNG reader for T35's guest frames (#682; T34's t34-png.py copied by git show from feature/m6-es-core-components-681): pixels by zlib and the
PNG filters, never by eye.
    t35-png.py row <png> <y> [x0 x1]     the RGB runs along row y
    t35-png.py px <png> <x> <y>...        the RGB at each point"""
import struct, sys, zlib

def read(path):
    b = open(path, "rb").read()
    assert b[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    i, idat, w = 8, b"", None
    while i < len(b):
        n, t = struct.unpack(">I4s", b[i:i + 8]); d = b[i + 8:i + 8 + n]; i += 12 + n
        if t == b"IHDR":
            w, h, depth, ctype = struct.unpack(">IIBB", d[:10])
            assert depth == 8 and ctype in (2, 6), (depth, ctype)
            bpp = 3 if ctype == 2 else 4
        elif t == b"IDAT":
            idat += d
    raw = zlib.decompress(idat); stride = w * bpp; rows, prev = [], bytearray(stride); p = 0
    for _ in range(h):
        f = raw[p]; line = bytearray(raw[p + 1:p + 1 + stride]); p += 1 + stride
        for x in range(stride):
            a = line[x - bpp] if x >= bpp else 0; up = prev[x]; c = prev[x - bpp] if x >= bpp else 0
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + up) & 255
            elif f == 3: line[x] = (line[x] + (a + up) // 2) & 255
            elif f == 4:
                pa, pb, pc = abs(up - c), abs(a - c), abs(a + up - 2 * c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else up if pb <= pc else c)) & 255
        rows.append(line); prev = line
    return w, h, bpp, rows

def rgb(img, x, y):
    w, h, bpp, rows = img
    return tuple(rows[y][x * bpp:x * bpp + 3])

if __name__ == "__main__":
    img = read(sys.argv[2])
    if sys.argv[1] == "row":
        y = int(sys.argv[3]); x0 = int(sys.argv[4]) if len(sys.argv) > 4 else 0; x1 = int(sys.argv[5]) if len(sys.argv) > 5 else img[0] - 1
        runs, start, cur = [], x0, rgb(img, x0, y)
        for x in range(x0 + 1, x1 + 2):
            c = rgb(img, x, y) if x <= x1 else None
            if c != cur:
                runs.append((start, x - 1, cur)); start, cur = x, c
        for a, b, c in runs:
            print("x %d-%d (%d px) rgb%s" % (a, b, b - a + 1, c))
    else:
        a = sys.argv[3:]
        for i in range(0, len(a), 2):
            print("(%s,%s) rgb%s" % (a[i], a[i + 1], rgb(img, int(a[i]), int(a[i + 1]))))
