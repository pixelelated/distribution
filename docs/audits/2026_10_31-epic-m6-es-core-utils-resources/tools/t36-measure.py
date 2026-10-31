"""Measure a text band's height in a frame, by a reader (stdlib zlib), not by eye.
Decodes a PNG (RGB/RGBA, 8-bit), then in a given y-range reports the contiguous run of
rows carrying 'ink' -- light pixels on the dark menu/help-bar background -- which is the
cap height of the text there. Used for G-02 (640x480) and G-06 (1280x800): the font's
scale at the two panel sizes.
    t36-measure.py <png> <y0> <y1> [<x0> <x1>] [--thresh N] [--minink K]
"""
import sys, zlib, struct

def read_png(path):
    d = open(path, "rb").read()
    assert d[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    i = 8; w = h = bd = ct = None; idat = b""
    while i < len(d):
        ln = struct.unpack(">I", d[i:i+4])[0]; typ = d[i+4:i+8]; body = d[i+8:i+8+ln]; i += 12 + ln
        if typ == b"IHDR":
            w, h, bd, ct = struct.unpack(">IIBB", body[:10])
        elif typ == b"IDAT":
            idat += body
        elif typ == b"IEND":
            break
    assert bd == 8, f"bit depth {bd} unsupported"
    ch = {0:1, 2:3, 3:1, 4:2, 6:4}[ct]
    raw = zlib.decompress(idat)
    stride = w * ch
    out = bytearray(w * h * ch)
    prev = bytearray(stride)
    pos = 0
    for y in range(h):
        f = raw[pos]; pos += 1
        line = bytearray(raw[pos:pos+stride]); pos += stride
        for x in range(stride):
            a = line[x-ch] if x >= ch else 0
            b = prev[x]
            c = line[x-ch] if False else (prev[x-ch] if x >= ch else 0)
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + b) & 255
            elif f == 3: line[x] = (line[x] + ((a + b) >> 1)) & 255
            elif f == 4:
                p = a + b - c; pa = abs(p-a); pb = abs(p-b); pc = abs(p-c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        out[y*stride:(y+1)*stride] = line
        prev = line
    return w, h, ch, out

def main():
    a = sys.argv[1:]
    png = a[0]; y0 = int(a[1]); y1 = int(a[2])
    x0 = int(a[3]) if len(a) > 4 and not a[3].startswith("--") else 0
    x1 = int(a[4]) if len(a) > 4 and not a[3].startswith("--") else None
    thresh = 140; minink = 3
    if "--thresh" in a: thresh = int(a[a.index("--thresh")+1])
    if "--minink" in a: minink = int(a[a.index("--minink")+1])
    w, h, ch, px = read_png(png)
    if x1 is None: x1 = w
    def lum(x, y):
        o = (y*w + x) * ch
        return (px[o]*299 + px[o+1]*587 + px[o+2]*114)//1000 if ch >= 3 else px[o]
    rows = []
    for y in range(max(0,y0), min(h,y1)):
        ink = sum(1 for x in range(x0, x1) if lum(x, y) >= thresh)
        rows.append((y, ink))
    # the longest contiguous run of rows with >= minink bright pixels
    best = (0, 0, 0); cur0 = None
    for y, ink in rows:
        if ink >= minink:
            if cur0 is None: cur0 = y
        else:
            if cur0 is not None:
                if y - cur0 > best[0]: best = (y - cur0, cur0, y-1)
                cur0 = None
    if cur0 is not None and rows and rows[-1][0] - cur0 + 1 > best[0]:
        best = (rows[-1][0] - cur0 + 1, cur0, rows[-1][0])
    print(f"{png}: {w}x{h} ch{ch}; band y[{y0},{y1}) x[{x0},{x1}) thresh{thresh}: "
          f"text run {best[0]} px (y {best[1]}..{best[2]})")

if __name__ == "__main__":
    main()
