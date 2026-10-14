#!/usr/bin/env python3
"""UNRUN offline stream inspection. Never extract files, create links or run payloads."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import socket
import stat
import struct
import sys
import time
import traceback
import zlib

HERE = Path(__file__).resolve().parent
CHUNK = 65536
REQUIRED_ELF = ('steamrtarm64/steam', 'steamrtarm64/steamclient.so')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_at(stream, offset, length, size):
    require(0 <= offset <= size and 0 <= length <= size - offset, f'Out-of-bounds read: {offset}+{length}/{size}')
    stream.seek(offset)
    raw = stream.read(length)
    require(len(raw) == length, f'Short read at {offset}: {len(raw)} != {length}')
    return raw


def elf_info(raw, name):
    """Parse in-memory bytes only; no loader, ldd, readelf, imports or filesystem lookup."""
    size = len(raw)
    require(size >= 64 and raw[:7] == b'\x7fELF\x02\x01\x01', f'{name}: expected ELF64 little-endian version 1')
    fields = struct.unpack_from('<16sHHIQQQIHHHHHH', raw)
    _, kind, machine, version, entry, phoff, _, _, ehsize, phsize, count, _, _, _ = fields
    require(kind in (2, 3) and machine == 183 and version == 1, f'{name}: type/machine/version {kind}/{machine}/{version}; require executable/shared AArch64')
    require(ehsize == 64 and phsize == 56 and 0 < count <= 128 and phoff + count * 56 <= size, f'{name}: unsupported program-header table')
    programs = []
    for index in range(count):
        typ, flags, offset, vaddr, _, filesz, memsz, align = struct.unpack_from('<IIQQQQQQ', raw, phoff + 56 * index)
        require(filesz == 0 or (offset <= size and filesz <= size - offset), f'{name}: program {index} exceeds file')
        if typ == 1:
            require(filesz <= memsz and (align in (0, 1) or (align & (align - 1)) == 0), f'{name}: invalid PT_LOAD size/alignment')
            require(align in (0, 1) or offset % align == vaddr % align, f'{name}: incongruent PT_LOAD offset/address')
        programs.append({'type': typ, 'flags': flags, 'offset': offset, 'vaddr': vaddr, 'filesz': filesz, 'memsz': memsz})
    loads = [p for p in programs if p['type'] == 1]
    require(loads, f'{name}: no PT_LOAD')
    interps = [p for p in programs if p['type'] == 3]
    require(len(interps) <= 1, f'{name}: multiple interpreters')
    interpreter = None
    if interps:
        p = interps[0]
        require(1 < p['filesz'] <= 4096, f'{name}: interpreter length out of bounds')
        text = bytes(raw[p['offset']:p['offset'] + p['filesz']])
        require(text.endswith(b'\0') and b'\0' not in text[:-1], f'{name}: malformed interpreter')
        interpreter = text[:-1].decode('ascii')
        require(interpreter.startswith('/') and '..' not in PurePosixPath(interpreter).parts, f'{name}: unsafe interpreter spelling')
    dynamics = [p for p in programs if p['type'] == 2]
    require(len(dynamics) <= 1, f'{name}: multiple dynamic tables')
    tags = []
    if dynamics:
        p = dynamics[0]
        require(0 < p['filesz'] <= 65536 and p['filesz'] % 16 == 0, f'{name}: dynamic table exceeds bound/alignment')
        terminated = False
        for pos in range(p['offset'], p['offset'] + p['filesz'], 16):
            tag, value = struct.unpack_from('<qQ', raw, pos)
            if tag == 0:
                terminated = True
                break
            tags.append((tag, value))
        require(terminated, f'{name}: dynamic table lacks DT_NULL')
    text_tags = [(tag, value) for tag, value in tags if tag in (1, 14, 15, 29)]
    strings = []
    if text_tags:
        addresses = [v for t, v in tags if t == 5]
        sizes = [v for t, v in tags if t == 10]
        require(len(addresses) == len(sizes) == 1 and 0 < sizes[0] <= 16 * 1024**2, f'{name}: ambiguous or oversized dynamic string table')
        address, length = addresses[0], sizes[0]
        matches = [p for p in loads if p['vaddr'] <= address and address + length <= p['vaddr'] + p['filesz']]
        require(len(matches) == 1, f'{name}: string table not uniquely file-backed by PT_LOAD')
        base = matches[0]['offset'] + address - matches[0]['vaddr']
        require(len(text_tags) <= 512, f'{name}: too many dynamic string references')
        for tag, offset in text_tags:
            require(offset < length, f'{name}: dynamic string offset outside table')
            end = raw.find(b'\0', base + offset, min(base + length, base + offset + 4097))
            require(end >= 0, f'{name}: dynamic string unterminated or >4096 bytes')
            strings.append({'tag': tag, 'value': bytes(raw[base + offset:end]).decode('utf-8')})
    entry_in_executable_load = any(p['flags'] & 1 and p['vaddr'] <= entry < p['vaddr'] + p['memsz'] for p in loads)
    if name == 'steamrtarm64/steam':
        require(entry > 0 and entry_in_executable_load, f'{name}: missing executable entry in an executable load segment')
    if name == 'steamrtarm64/steamclient.so':
        require(kind == 3, f'{name}: expected ET_DYN shared library')
    return {'class': 64, 'endianness': 'little', 'machine': machine, 'type': kind, 'entry': entry,
            'entry_in_executable_load': entry_in_executable_load, 'interpreter': interpreter,
            'needed': [r['value'] for r in strings if r['tag'] == 1],
            'soname': [r['value'] for r in strings if r['tag'] == 14],
            'rpath': [r['value'] for r in strings if r['tag'] == 15],
            'runpath': [r['value'] for r in strings if r['tag'] == 29],
            'program_headers': len(programs), 'dynamic_table_present': bool(dynamics), 'external_resolution': 'UNPROVEN; no target loader or filesystem consulted'}


def inventory(stream, size, members, ownership, end):
    central = read_at(stream, end['central_offset'], end['central_bytes'], size)
    require(central == (HERE / 'bound/central.bin').read_bytes(), 'Central-directory bytes differ from sealed 49a586 inventory')
    require(read_at(stream, 0, 20, size) == (HERE / 'bound/prefix.bin').read_bytes(), 'Opaque 20-byte prefix changed')
    eocd = struct.unpack('<4s4H2IH', read_at(stream, size - 22, 22, size))
    require(eocd == (b'PK\x05\x06', 0, 0, 55, 55, 4146, 110369493, 0), f'Unadvertised EOCD/ZIP64/comment: {eocd!r}')
    require(len(members) == len(ownership['members']) == 55, 'Expected 55 advertised entries')
    names, folded = {}, set()
    for advertised, row in zip(members, ownership['members']):
        raw_name, canonical = advertised['name'], row['canonical_name']
        require(row['raw_name'] == raw_name and row['kind'] == advertised['kind'], 'Ownership inventory mismatch')
        changes = {item['raw_name']: item['canonical_name'] for item in ownership['names_changed']}
        require(len(changes) == 5 and canonical == changes.get(raw_name, raw_name), f'Unexpected normalization for {raw_name!r}')
        require('\\' not in canonical and ':' not in canonical and '\0' not in canonical, f'Unsafe canonical spelling {canonical!r}')
        parts = canonical.rstrip('/').split('/')
        require(len(parts) >= 2 and parts[0] == 'steamrtarm64' and all(p not in ('', '.', '..') for p in parts), f'Outside owned tree: {canonical!r}')
        key = '/'.join(parts)
        require(key not in names and key.casefold() not in folded, f'Duplicate/case collision {canonical!r}')
        names[key] = advertised['kind']; folded.add(key.casefold())
    for name in names:
        parts = name.split('/')
        for index in range(1, len(parts)):
            parent = '/'.join(parts[:index])
            require(names.get(parent, 'directory') == 'directory', f'Non-directory canonical ancestor {parent!r}')
    rows, position, last_end = [], 0, 20
    for advertised, mapped in zip(members, ownership['members']):
        fields = struct.unpack_from('<4s6H3I5H2I', central, position)
        sig, made, needed, flags, method, mtime, mdate, crc, packed, unpacked, nlen, extra, comment, disk, _, external, local = fields
        name = bytes.fromhex(advertised['name_hex'])
        require(sig == b'PK\x01\x02' and disk == flags == extra == comment == 0, f'{advertised["name"]}: unsupported central flags/extra/disk/comment')
        require(central[position + 46:position + 46 + nlen] == name, f'{advertised["name"]}: central name mismatch')
        observed = (made, needed, method, crc, packed, unpacked, external, local)
        wanted = (advertised['version_made_by'], advertised['version_needed'], advertised['compression_method'], int(advertised['crc32'], 16), advertised['compressed_bytes'], advertised['uncompressed_bytes'], advertised['external_attributes'], advertised['local_header_offset'])
        require(observed == wanted, f'{advertised["name"]}: unadvertised central fields {observed!r}')
        require(local == last_end, f'{advertised["name"]}: gap/overlap/unadvertised local member at {local}; expected {last_end}')
        header = struct.unpack('<4s5H3I2H', read_at(stream, local, 30, size))
        require(header == (b'PK\x03\x04', needed, flags, method, mtime, mdate, crc, packed, unpacked, nlen, 0), f'{advertised["name"]}: local fields differ from central: {header!r}')
        require(read_at(stream, local + 30, nlen, size) == name, f'{advertised["name"]}: local name mismatch')
        data_offset = local + 30 + nlen
        last_end = data_offset + packed
        require(last_end <= end['central_offset'], f'{advertised["name"]}: compressed bytes overlap central directory')
        rows.append(dict(advertised, canonical_name=mapped['canonical_name'], data_offset=data_offset))
        position += 46 + nlen
    require(position == len(central) and last_end == end['central_offset'], 'Unadvertised bytes before central directory/end record')
    return rows


def scan_member(stream, row, limits, totals):
    name, expected = row['name'], row['uncompressed_bytes']
    require(expected <= limits['member_bytes'], f'{name}: advertised member exceeds allocation')
    stream.seek(row['data_offset'])
    remaining, actual, crc = row['compressed_bytes'], 0, 0
    checksum = hashlib.sha256()
    prefix, elf_bytes, link_bytes = bytearray(), None, bytearray()
    classified = False
    decoder = zlib.decompressobj(-15) if row['compression_method'] == 8 else None
    require(row['compression_method'] in (0, 8), f'{name}: unreviewed method')

    def accept(chunk):
        nonlocal actual, crc, elf_bytes, classified
        actual += len(chunk); totals['decoded_bytes'] += len(chunk)
        require(actual <= expected and totals['decoded_bytes'] <= limits['decoded_bytes'], f'{name}: decoded bytes exceed declared/global bound')
        crc = zlib.crc32(chunk, crc); checksum.update(chunk)
        if not classified:
            take = min(4 - len(prefix), len(chunk))
            prefix.extend(chunk[:take])
            if len(prefix) == 4:
                classified = True
                if prefix == b'\x7fELF':
                    elf_bytes = bytearray(prefix)
                    elf_bytes.extend(chunk[take:])
        elif elf_bytes is not None:
            elf_bytes.extend(chunk)  # At most one <=128MiB member in memory, never a payload file.
        if row['kind'] == 'symlink':
            require(actual <= 4096, f'{name}: oversized link text')
            link_bytes.extend(chunk)

    while remaining:
        packed = stream.read(min(CHUNK, remaining))
        require(packed, f'{name}: short compressed read')
        remaining -= len(packed)
        if decoder is None:
            accept(packed)
            continue
        pending = packed
        while True:
            decoded = decoder.decompress(pending, CHUNK)
            accept(decoded)
            pending = decoder.unconsumed_tail
            require(not decoder.unused_data, f'{name}: trailing data inside advertised deflate span')
            if not pending and len(decoded) < CHUNK:
                break
            require(decoded or pending, f'{name}: stalled deflate decoder')
    if decoder is not None:
        require(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail, f'{name}: truncated/unfinished deflate stream')
    require(actual == expected and crc == int(row['crc32'], 16), f'{name}: length/CRC got {actual}/{crc:08x}, expected {expected}/{row["crc32"]}')
    result = {'raw_name': name, 'canonical_name': row['canonical_name'], 'kind': row['kind'], 'bytes': actual,
              'sha256': checksum.hexdigest(), 'crc32': f'{crc:08x}', 'compressed_bytes': row['compressed_bytes']}
    if row['kind'] == 'symlink':
        result['relative_target'] = link_bytes.decode('ascii')
    if elf_bytes is not None:
        result['elf'] = elf_info(elf_bytes, row['canonical_name'])
    elif row['canonical_name'] in REQUIRED_ELF:
        raise ValueError(f'{name}: required bootstrap member is not ELF')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive-fd', required=True, type=int)
    parser.add_argument('--receipt', required=True, type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    report = {'status': 'FAIL', 'evidence': 'Full archive integrity and nonexecuting structural inspection only',
              'python': sys.version, 'zlib_build': zlib.ZLIB_VERSION, 'zlib_runtime': zlib.ZLIB_RUNTIME_VERSION,
              'members': [], 'signature_verification': 'UNVERIFIED', 'native_readiness': 'UNPROVEN'}
    try:
        def deny(event, _args):
            if event.startswith(('socket.', 'subprocess.', 'os.exec', 'os.spawn', 'os.fork')):
                raise RuntimeError('Offline inspector denies network/process creation: ' + event)
        sys.addaudithook(deny)
        try:
            socket.socket()
        except RuntimeError as error:
            require(str(error).startswith('Offline inspector denies'), 'Unexpected socket-denial exception')
            report['socket_denial_control'] = 'PASS'
        else:
            raise RuntimeError('Socket denial did not fail closed')
        binding = json.loads((HERE / 'source.json').read_bytes())
        for name, expected in binding['bound_files'].items():
            require(digest((HERE / name).read_bytes()) == expected, f'Bound metadata changed: {name}')
        selected = json.loads((HERE / 'bound/selected.json').read_bytes())
        members = json.loads((HERE / 'bound/members.json').read_bytes())
        ownership = json.loads((HERE / 'bound/ownership-plan.json').read_bytes())
        end = json.loads((HERE / 'bound/zip-end.json').read_bytes())
        limits = binding['limits']
        require(len(members) <= limits['entries'], 'Advertised entries exceed limit')
        with os.fdopen(args.archive_fd, 'rb', closefd=False) as stream:
            before = os.fstat(stream.fileno())
            require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size == selected['size'], 'Archive must be a single-link regular file of exact advertised size')
            checksum = hashlib.sha256()
            while chunk := stream.read(CHUNK):
                checksum.update(chunk)
            report['archive_sha256'] = checksum.hexdigest()
            require(checksum.hexdigest() == selected['sha256_from_manifest'], 'Full archive SHA256 differs; no decoding performed')
            report['full_hash_before_decode'] = True
            rows = inventory(stream, before.st_size, members, ownership, end)
            totals = {'decoded_bytes': 0}
            for row in rows:
                result = scan_member(stream, row, limits, totals)
                report['members'].append(result)
            require(totals['decoded_bytes'] == 339635561, 'Decoded total differs from advertised inventory')
            for link in ownership['stored_links']:
                result = next(r for r in report['members'] if r['raw_name'] == link['raw_name'])
                require(result.get('relative_target') == link['relative_target'], f'Link payload differs: {link["raw_name"]}')
                require('/' not in link['relative_target'] and '\\' not in link['relative_target'] and link['relative_target'] not in ('.', '..'), 'Non-basename link target')
                target = str(PurePosixPath(result['canonical_name']).parent / link['relative_target'])
                require(target == link['canonical_target'] and any(r['canonical_name'] == target and r['kind'] == 'regular' for r in rows), 'Link target is not an advertised regular member')
            after = os.fstat(stream.fileno())
            require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) ==
                    (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns), 'Archive identity changed during scan')
        report.update(status='PASS', decoded_bytes=totals['decoded_bytes'], archive_bytes=before.st_size,
                      modeled_name_changes=ownership['names_changed'], required_elf_structure='PASS',
                      symlinks_created=0, payload_files_created=0, payloads_executed=0,
                      limits=limits, external_dependency_resolution='UNPROVEN; needed/interpreter strings reported only')
    except BaseException as error:
        report.update(error=repr(error), traceback=traceback.format_exc(limit=8))
    report['elapsed_seconds'] = time.monotonic() - started
    raw = (json.dumps(report, indent=2) + '\n').encode()
    require(len(raw) <= 4 * 1024**2, 'Inspection receipt exceeds 4MiB')
    with args.receipt.open('xb') as output:
        output.write(raw)
    print(json.dumps({'status': report['status'], 'completed_members': len(report['members']), 'error': report.get('error')}))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
