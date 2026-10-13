#!/usr/bin/env python3
"""UNRUN: create <=32 MiB of synthetic, non-bootable GC ISO/RVZ controls.

No ROM input, network, subprocess, or emulator. Uses stdlib and the target's
existing libzstd via ctypes. The output directory must not already exist.
Padding algorithm adapted from bodgit/rvz, BSD-3-Clause; see upstream license.
"""
import argparse
import ctypes
import hashlib
import json
from pathlib import Path
import struct


def u32(data, offset):
    return struct.unpack_from('>I', data, offset)[0]


def put32(data, offset, value):
    struct.pack_into('>I', data, offset, value)


def put64(data, offset, value):
    struct.pack_into('>Q', data, offset, value)


def padding(seed, offset, length):
    words = list(struct.unpack('>17I', seed))
    for i in range(17, 521):
        words.append(((words[i - 17] << 23) ^ (words[i - 16] >> 9) ^ words[i - 1]) & 0xffffffff)

    def advance():
        for i in range(521):
            words[i] ^= words[(i - 32) % 521]

    for _ in range(4):
        advance()
    skip = offset % 0x8000
    output = bytearray()
    while len(output) < skip + length:
        for word in words:
            output.extend((word >> shift) & 255 for shift in (24, 18, 8, 0))
        advance()
    return bytes(output[skip:skip + length])


class Zstd:
    def __init__(self, library):
        self.lib = ctypes.CDLL(library)
        self.lib.ZSTD_compressBound.argtypes = [ctypes.c_size_t]
        self.lib.ZSTD_compressBound.restype = ctypes.c_size_t
        self.lib.ZSTD_compress.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                                          ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int]
        self.lib.ZSTD_compress.restype = ctypes.c_size_t
        self.lib.ZSTD_isError.argtypes = [ctypes.c_size_t]
        self.lib.ZSTD_isError.restype = ctypes.c_uint

    def compress(self, data):
        source = ctypes.create_string_buffer(data)
        dest = ctypes.create_string_buffer(self.lib.ZSTD_compressBound(len(data)))
        size = self.lib.ZSTD_compress(dest, len(dest), source, len(data), 3)
        if self.lib.ZSTD_isError(size):
            raise RuntimeError('Synthetic Zstandard compression failed')
        return dest.raw[:size]


SEED = bytes((i * 7 + 3) & 255 for i in range(68))
JUNK_AT, JUNK_SIZE = 0x38013, 0x1234


def raw_disc():
    raw = bytearray(0x60000)
    raw[:6] = b'PX5740'
    put32(raw, 0x1c, 0xc2339f3d)
    label = b'pixelelated synthetic #574!!\0'
    raw[0x20:0x20 + len(label)] = label
    put32(raw, 0x420, 0x10000)
    put32(raw, 0x2440 + 0x14, 0x180)
    put32(raw, 0x2440 + 0x18, 0x80)
    for slot, (offset, size) in enumerate(((0x1ffe0, 0x500), (0x38020, 0x600), (0x50010, 0x100))):
        put32(raw, 0x10000 + slot * 4, offset)
        put32(raw, 0x10000 + 0x90 + slot * 4, size)
        if slot < 2:
            raw[offset:offset + size] = bytes((i * 11 + slot) & 255 for i in range(size))
    raw[JUNK_AT:JUNK_AT + JUNK_SIZE] = padding(SEED, JUNK_AT, JUNK_SIZE)
    return raw


def oracle(raw):
    # Independent byte-range MD5 oracle for this non-bootable synthetic layout.
    return hashlib.md5(raw[:0x2660] + raw[0x1ffe0:0x204e0] +
                       raw[0x38020:0x38620] + raw[0x50010:0x50110]).hexdigest()


def seal(data):
    put64(data, 0x2c, len(data))
    second_size = u32(data, 0xc)
    data[0x10:0x24] = hashlib.sha1(data[0x48:0x48 + second_size]).digest()
    data[0x34:0x48] = hashlib.sha1(data[:0x34]).digest()
    return data


def rvz(raw, compressor=None, packed=False, store_first=False):
    data = bytearray(0x48 + 0xdc)
    data[:4] = b'RVZ\x01'
    put32(data, 4, 0x01000000)
    put32(data, 8, 0x00030000)
    put32(data, 0xc, 0xdc)
    put64(data, 0x24, len(raw))
    put32(data, 0x48, 1)
    put32(data, 0x48 + 4, 5 if compressor else 0)
    put32(data, 0x48 + 8, 3 if compressor else 0)
    put32(data, 0x48 + 12, 0x20000)
    data[0x58:0xd8] = raw[:0x80]
    groups, regions, locations = [], [], []
    for begin, end in ((0, 0x30000), (0x30000, len(raw))):
        first = len(groups)
        for at in range(begin, end, 0x20000):
            block = bytes(raw[at:min(at + 0x20000, end)])
            unpacked_size = 0
            if not any(block):
                groups.append(struct.pack('>III', 0, 0, 0))
                locations.append(None)
                continue
            if packed and at <= JUNK_AT and JUNK_AT + JUNK_SIZE <= at + len(block):
                prefix = JUNK_AT - at
                suffix = prefix + JUNK_SIZE
                block = (struct.pack('>I', prefix) + block[:prefix] +
                         struct.pack('>I', 0x80000000 | JUNK_SIZE) + SEED +
                         struct.pack('>I', len(block) - suffix) + block[suffix:])
                unpacked_size = len(block)
            encoded = compressor.compress(block) if compressor else block
            compressed = bool(compressor and len(encoded) < len(block) and
                              not (store_first and not groups))
            if not compressed:
                encoded = block
            data.extend(b'\0' * (-len(data) % 4))
            locations.append(len(data))
            groups.append(struct.pack('>III', len(data) // 4,
                                      len(encoded) | (0x80000000 if compressed else 0), unpacked_size))
            data.extend(encoded)
        offset = begin or 0x80
        regions.append(struct.pack('>QQII', offset, end - offset, first, len(groups) - first))
    for header_count, header_offset, header_size, entries in (
            (0xb4, 0xb8, 0xc0, regions), (0xc4, 0xc8, 0xd0, groups)):
        table = b''.join(entries)
        if compressor:
            table = compressor.compress(table)
        put32(data, 0x48 + header_count, len(entries))
        put64(data, 0x48 + header_offset, len(data))
        put32(data, 0x48 + header_size, len(table))
        data.extend(table)
    return seal(data), locations


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--zstd-library', default='libzstd.so.1')
    args = parser.parse_args()
    zstd = Zstd(args.zstd_library)
    raw = raw_disc()
    digest = oracle(raw)
    none, locations = rvz(raw)
    packed, packed_locations = rvz(raw, packed=True)
    compressed, compressed_locations = rvz(raw, zstd, packed=True)
    cases = []

    def add(name, data, expected=None, baseline=None, console='gamecube'):
        cases.append(dict(name=name, data=bytes(data), expected=expected,
                          baseline=baseline, console=console))

    def edit(source, offset, value, reseal=False):
        data = bytearray(source)
        put32(data, offset, value)
        return seal(data) if reseal else data

    add('synthetic.iso', raw, digest, digest)
    for name, data in (('none.rvz', none), ('packed-none.rvz', packed),
                       ('packed-zstd.rvz', compressed), ('uppercase.RVZ', compressed),
                       ('mixed-zstd.rvz', rvz(raw, zstd, store_first=True)[0])):
        add(name, data, digest, 'FAIL')
    plain = b'pixelelated synthetic non-disc hashing regression\n'
    add('ordinary.nes', plain, hashlib.md5(plain).hexdigest(), hashlib.md5(plain).hexdigest(), 'nes')
    add('empty.iso', b'')
    add('short-magic.iso', raw[:0x1e])
    add('short-apploader.iso', raw[:0x2456])
    add('short-dol.iso', raw[:0x10020])
    add('short-section.iso', raw[:0x20100])
    add('bad-magic.rvz', edit(none, 0, 0))
    add('short-header.rvz', none[:0x47])
    add('short-second-header.rvz', none[:0x100])
    add('short-container.rvz', none[:-3])
    add('bad-header-sha1.rvz', edit(none, 0x34, 0))
    add('bad-second-sha1.rvz', edit(none, 0x48 + 8, 7))
    for name, offset, value in (
            ('unsupported-compression', 4, 3), ('unsupported-wii', 0, 2),
            ('oversized-chunk', 0xc, 0x400000), ('oversized-raw-count', 0xb4, 0xffffffff),
            ('oversized-group-count', 0xc4, 0xffffffff)):
        add(name + '.rvz', edit(none, 0x48 + offset, value, True))
    add('oversized-disc.rvz', edit(none, 0x24, 0xffffffff, True))
    group_table = struct.unpack_from('>Q', none, 0x48 + 0xc8)[0]
    add('group-outside-file.rvz', edit(none, group_table, 0xffffffff))
    raw_table = struct.unpack_from('>Q', none, 0x48 + 0xb8)[0]
    add('group-index-outside-table.rvz', edit(none, raw_table + 16, 0xffffffff))
    add('packed-overflow.rvz', edit(packed, packed_locations[2], 0x7fffffff))
    add('corrupt-zstd.rvz', edit(compressed, compressed_locations[0], 0))
    bad_dol = bytearray(raw)
    put32(bad_dol, 0x10000, len(raw) - 8)
    add('section-outside-disc.iso', bad_dol)
    add('section-outside-disc.rvz', rvz(bad_dol, zstd, packed=True)[0])
    assert sum(len(c['data']) for c in cases) <= 32 * 1024 * 1024
    args.output.mkdir(parents=False, exist_ok=False)
    manifest = []
    for case in cases:
        data = case.pop('data')
        (args.output / case['name']).write_bytes(data)
        case['sha256'] = hashlib.sha256(data).hexdigest()
        case['bytes'] = len(data)
        manifest.append(case)
    (args.output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(dict(cases=len(cases), total_bytes=sum(c['bytes'] for c in manifest), oracle=digest)))


if __name__ == '__main__':
    main()
