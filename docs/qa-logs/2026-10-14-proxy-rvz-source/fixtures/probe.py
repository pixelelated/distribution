#!/usr/bin/env python3
"""UNRUN: bounded VM source controls; no proxy imports, listener or native hasher.

Execute actual sealed list_jobs heredocs with declared synthetic import adapters,
and actual RVZ Python modules with native codecs refused. Never execute the ctl shell.
"""
from __future__ import annotations
import argparse
import ast
import contextlib
import dataclasses
import hashlib
import io
import json
import os
from pathlib import Path
import resource
import signal
import socket
import sqlite3
import struct
import sys
import time
import types
import xml.etree.ElementTree as ET

PACKET = Path(__file__).resolve().parents[1]
INPUTS_SHA256 = '613cad28a49000fb0e348798be4e88b319c7348e635e0617c813b6a7392e91b3'
ZERO = '0' * 32
GOOD = '0123456789abcdef' * 2
USER = 'fixture-user'


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def module(name, **values):
    result = types.ModuleType(name)
    result.__dict__.update(values)
    sys.modules[name] = result
    return result


def selected_functions(path, names, values):
    tree = ast.parse(path.read_text())
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
    need({node.name for node in nodes} == set(names), f'missing sealed functions: {path}')
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), values)
    return values


def spec_bytes(seed, size):
    """Independent full-stream oracle from retained Dolphin format specification.

    Produces complete buffers before slicing; does not reuse proxy writer/skip code.
    Native Dolphin parity is still a separate VM gate.
    """
    state = list(seed) + [0] * (521 - len(seed))
    for i in range(17, 521):
        state[i] = ((state[i-17] << 23) ^ (state[i-16] >> 9) ^ state[i-1]) & 0xffffffff
    def advance():
        for i in range(521):
            state[i] ^= state[(i + 489) % 521]
    for _ in range(4):
        advance()
    stream = bytearray()
    while len(stream) < size:
        for value in state:
            stream.extend(((value >> 24) & 255, (value >> 18) & 255,
                           (value >> 8) & 255, value & 255))
        advance()
    return bytes(stream[:size])


def rvz_bytes(packed, logical_size=32768, compression=0):
    """Small nonbootable GameCube-tagged NONE container, real RVZ table layout."""
    h2 = bytearray(0xd5)
    raw_at = (0x48 + len(h2) + 3) & ~3
    groups_at = raw_at + 24
    data_at = groups_at + 12
    struct.pack_into('>IIII', h2, 0, 1, compression, 0, 32768)
    h2[0x10:0x16] = b'GQAE01'
    struct.pack_into('>I', h2, 0x10 + 0x1c, 0xc2339f3d)
    struct.pack_into('>I', h2, 0x94, 0x30)
    h2[0xa0:0xb4] = hashlib.sha1(b'').digest()
    struct.pack_into('>I', h2, 0xb4, 1)
    struct.pack_into('>Q', h2, 0xb8, raw_at)
    struct.pack_into('>I', h2, 0xc0, 24)
    struct.pack_into('>I', h2, 0xc4, 1)
    struct.pack_into('>Q', h2, 0xc8, groups_at)
    struct.pack_into('>I', h2, 0xd0, 12)
    raw = struct.pack('>QQII', 0x80, logical_size - 0x80, 0, 1)
    group = struct.pack('>III', data_at // 4, len(packed), len(packed))
    h1 = bytearray(0x48)
    h1[:4] = b'RVZ\x01'
    struct.pack_into('>III', h1, 4, 0x01000000, 0x00030000, len(h2))
    h1[0x10:0x24] = hashlib.sha1(h2).digest()
    struct.pack_into('>QQ', h1, 0x24, logical_size, data_at + len(packed))
    h1[0x34:] = hashlib.sha1(h1[:0x34]).digest()
    return bytes(h1 + h2).ljust(raw_at, b'\0') + raw + group + packed


class MemorySource:
    def __init__(self, value):
        self.value = value
    def read(self, offset, length):
        return self.value[offset:offset+length]


def check_rvz(records):
    def no_codec(*args):
        raise RuntimeError('native codec execution not allocated by this source fixture')
    for variant in ('source', 'candidates'):
        package = 'rvz_fixture_' + variant
        module(package, __path__=[])
        module(package + '.native_codecs', CodecError=RuntimeError,
               zstd_decompress=no_codec, zstd_frame_content_size=no_codec,
               aes_128_cbc_encrypt=no_codec)
        impl = module(package + '.rvz_datasource', __package__=package)
        source = PACKET / variant / 'rvz_datasource.py'
        exec(compile(source.read_bytes(), str(source), 'exec'), impl.__dict__)
        aligned = unaligned = mismatches = 0
        seeds = [list(range(17)), [0x12345678 ^ (i * 0x01010101) for i in range(17)],
                 [0xffffffff - i for i in range(17)]]
        offsets = (0, 1, 2, 3, 4, 2083, 2084, 2085, 32767, 32768, 32769)
        lengths = (1, 2, 3, 4, 17, 2085)
        for seed in seeds:
            oracle = spec_bytes(seed, 32768 + max(lengths))
            for offset in offsets:
                for size in lengths:
                    actual = impl._generate_rvz_bytes(seed, size, offset)
                    expected = oracle[offset % 32768:offset % 32768 + size]
                    match = actual == expected
                    if offset % 4 == 0:
                        aligned += 1
                        need(match, f'{variant}: aligned padding mismatch offset={offset} size={size}')
                    else:
                        unaligned += 1
                        mismatches += not match
                        if variant == 'candidates':
                            need(match, f'candidate padding mismatch offset={offset} size={size}')
        if variant == 'source':
            need(mismatches > 0, 'old-source padding defect did not reproduce')
        seed = seeds[1]
        packed = struct.pack('>I', 1) + b'X' + struct.pack('>I', 0x80000000 | 32767)
        packed += struct.pack('>17I', *seed)
        image = rvz_bytes(packed)
        parsed = impl.RvzDataSource.open(MemorySource(image))
        need(parsed is not None, f'{variant}: valid synthetic RVZ rejected')
        expected = spec_bytes(seed, 32768)[0x80:]
        full_match = parsed.read(0x80, 32768 - 0x80) == expected
        need(full_match == (variant == 'candidates'), f'{variant}: packed RVZ byte oracle mismatch')
        for name, bad in [('empty', b''), ('short', image[:47]),
                          ('magic', b'BAD!' + image[4:]),
                          ('header-sha', image[:40] + bytes([image[40] ^ 1]) + image[41:]),
                          ('unsupported-bzip2', rvz_bytes(packed, compression=2))]:
            need(impl.RvzDataSource.open(MemorySource(bad)) is None,
                 f'{variant}: {name} incorrectly accepted')
        truncated = impl.RvzDataSource.open(MemorySource(image[:-1]))
        need(truncated is not None, f'{variant}: truncation fixture lost its valid header')
        try:
            truncated.read(0x80, 128)
        except impl.RvzParseError:
            pass
        else:
            raise AssertionError(f'{variant}: truncated RVZ group was silently accepted')
        records.append({'variant': variant, 'aligned_controls': aligned,
                        'unaligned_comparisons': unaligned, 'mismatches': mismatches,
                        'packed_rvz_matches_oracle': full_match, 'invalid_controls': 6,
                        'source_sha256': digest(source.read_bytes())})
    return records


def check_listing(output, records):
    package = module('raofflineproxy', __path__=[])
    keys = module('raofflineproxy.cache_keys')
    path = PACKET / 'source/cache_keys.py'
    exec(compile(path.read_bytes(), str(path), 'exec'), keys.__dict__)
    package.cache_keys = keys
    funcs = {'Path': Path}
    selected_functions(PACKET/'source/rom_hashing.py', ['supported_rom_extensions'], funcs)
    funcs['SUPPORTED_ROM_EXTENSIONS'] = funcs['supported_rom_extensions']()
    funcs['SUPPORTED_ARCHIVE_EXTENSIONS'] = {'.zip', '.7z'}
    selected_functions(PACKET/'source/rom_browser.py',
                       ['is_supported_browser_file', 'normalize_cached_rom_path'], funcs)
    # Small cap is intentional injection to exercise production cursor code cheaply.
    module('raofflineproxy.rom_browser', MAX_SCAN_ENTRIES=2,
           is_supported_browser_file=funcs['is_supported_browser_file'],
           normalize_cached_rom_path=funcs['normalize_cached_rom_path'])
    cases = ('failed', 'mixed', 'cached', 'partial-cache', 'other-account',
             'recovery', 'stale-recovery', 'cursor', 'unindexed', 'missing-empty')
    for variant in ('source', 'candidates'):
        for case in cases:
            for mode in ('all', 'indexed'):
                root = output / f'{variant}-{case}-{mode}'
                root.mkdir()
                roms = root/'roms'; folder = roms/'gamecube'; folder.mkdir(parents=True)
                es = root/'es'; es.mkdir()
                (es/'es_systems_custom.cfg').write_text(
                    '<systemList><system><name>gamecube</name><path>'+str(folder)+'</path></system></systemList>')
                entries = [('A.rvz', ZERO, '')]
                if case == 'mixed':
                    entries += [('B.RVZ', GOOD, '42'), ('C.rvz', GOOD, ''),
                                ('D.rvz', '', ''), ('E.iso', ZERO, ''),
                                ('F.rvz', ZERO, '99')]
                if case in ('cached', 'partial-cache', 'other-account'):
                    entries += [('B.rvz', GOOD, '42')]
                if case == 'cursor':
                    entries += [('B.rvz', ZERO, ''), ('C.rvz', ZERO, '')]
                if case == 'unindexed':
                    entries = [('A.rvz', '', '')]
                xml = ET.Element('gameList')
                for filename, h, gid in entries:
                    (folder/filename).write_bytes(b'fixture file, not hashed by listing')
                    game = ET.SubElement(xml, 'game')
                    for key, val in [('path', './'+filename), ('cheevosHash', h), ('cheevosId', gid)]:
                        ET.SubElement(game, key).text = val
                gamelist = folder/'gamelist.xml'; ET.ElementTree(xml).write(gamelist)
                if case == 'missing-empty':
                    (folder/'A.rvz').write_bytes(b'')
                if case in ('recovery', 'stale-recovery'):
                    recovery = es/'recovery/gamecube'; recovery.mkdir(parents=True)
                    doc = ET.Element('gameList', parentHash=str(gamelist.stat().st_size + (case == 'stale-recovery')))
                    item = ET.SubElement(doc, 'game')
                    for key, val in [('path', './A.rvz'), ('cheevosHash', GOOD), ('cheevosId', '42')]:
                        ET.SubElement(item, key).text = val
                    ET.ElementTree(doc).write(recovery/'A.xml')
                rows = []
                if case in ('cached', 'partial-cache', 'other-account'):
                    account = USER if case != 'other-account' else 'different-fixture-user'
                    rows = [dict(cacheKey=keys.patch(42, account), responseBody='{"PatchData":{"ID":42}}',
                                 sourceRomPath='/gamecube/A.rvz'),
                            dict(cacheKey=keys.unlocks(42, account), responseBody='{"UserUnlocks":[]}', sourceRomPath=None)]
                    if case != 'partial-cache':
                        rows.append(dict(cacheKey=keys.achievementsets(GOOD, account),
                                         responseBody='{"GameId":42}', sourceRomPath=None))
                database = root/'synthetic.sqlite3'
                with sqlite3.connect(database) as db:
                    db.execute('CREATE TABLE api_cache (cacheKey TEXT PRIMARY KEY,responseBody TEXT,sourceRomPath TEXT)')
                    db.executemany('INSERT INTO api_cache VALUES (:cacheKey,:responseBody,:sourceRomPath)', rows)
                    db.execute('CREATE TABLE pending_awards (sentinel TEXT)')
                    db.execute("INSERT INTO pending_awards VALUES ('never upload this synthetic sentinel')")
                class FakeStorage:
                    def get_cache(self, key):
                        return next((r for r in rows if r['cacheKey'] == key), None)
                    def iter_cache_by_prefix(self, prefix):
                        return (r for r in rows if r['cacheKey'].startswith(prefix))
                    def cache_summaries_by_prefix(self, prefix):
                        return self.iter_cache_by_prefix(prefix)
                    def close(self):
                        pass
                module('raofflineproxy.storage', Storage=FakeStorage)
                module('raofflineproxy.config', DATABASE_FILE=database, load_config=lambda: {})
                module('raofflineproxy.smart_cache', load_content_history_paths=lambda config: [])
                job_file = root/'jobs'; cursor = root/'cursor'
                if case == 'cursor':
                    cursor.write_text(str(folder/'B.rvz')+'\n')
                protected = [p for p in root.rglob('*') if p.is_file()]
                before = {str(p): digest(p.read_bytes()) for p in protected}
                previous = sys.argv
                sys.argv = ['list_jobs', str(job_file), mode, str(roms), str(es), 'gamecube', str(cursor)]
                os.environ['RA_SCAN_USER'] = USER
                buf = io.StringIO()
                program = PACKET/variant/'list_jobs.py'
                try:
                    with contextlib.redirect_stdout(buf):
                        exec(compile(program.read_bytes(), str(program), 'exec'), {'__name__': '__main__'})
                finally:
                    sys.argv = previous
                need(before == {str(p): digest(p.read_bytes()) for p in protected},
                     f'{variant}/{case}/{mode}: existing fixture bytes changed')
                jobs = [line.split('\t', 3) for line in job_file.read_text().splitlines()]
                got = {(j[0], Path(j[3]).name) for j in jobs}
                expected = set()
                if case in ('mixed', 'partial-cache', 'other-account'):
                    expected.add(('I', 'B.RVZ' if case == 'mixed' else 'B.rvz'))
                if case == 'recovery':
                    expected.add(('I', 'A.rvz'))
                if case == 'mixed' and variant == 'source':
                    expected.add(('I', 'F.rvz'))  # old sentinel+id accepted: retained negative evidence
                recovery_case = case not in ('cached', 'recovery', 'unindexed', 'missing-empty')
                if mode == 'all' and variant == 'candidates' and recovery_case:
                    expected.add(('H', 'A.rvz'))
                    if case == 'mixed': expected.add(('H', 'F.rvz'))
                    if case == 'cursor': expected.add(('H', 'C.rvz'))
                if mode == 'all' and case == 'unindexed':
                    expected.add(('H', 'A.rvz'))
                need(got == expected, f'{variant}/{case}/{mode}: jobs={sorted(got)} expected={sorted(expected)}')
                need(len(jobs) == len(got), f'{variant}/{case}/{mode}: duplicate jobs')
                if case == 'cursor' and variant == 'candidates' and mode == 'all':
                    need([Path(j[3]).name for j in jobs] == ['C.rvz', 'A.rvz'], 'cursor order changed')
                    need('truncated=1' in buf.getvalue(), 'cursor truncation not reported')
                    need(cursor.with_name('cursor.next').read_text().strip() == str(folder/'A.rvz'), 'cursor proposal incorrect')
                records.append({'variant': variant, 'case': case, 'mode': mode,
                                'jobs': sorted(got), 'stdout': buf.getvalue(),
                                'original_exit': 0, 'protected_files_unchanged': len(protected)})
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    output = args.output.absolute()
    need(output.parent == Path('/run') and output.name.startswith('pix583-'),
         'use a fresh /run/pix583-* directory in the allocated disposable VM')
    need(not output.exists() and not output.is_symlink(), 'output already exists')
    manifest_bytes = (PACKET/'fixture-inputs.json').read_bytes()
    need(digest(manifest_bytes) == INPUTS_SHA256, 'fixture input manifest identity changed')
    identities = json.loads(manifest_bytes)
    for relative, expected in identities.items():
        need(digest((PACKET/relative).read_bytes()) == expected, 'source identity changed: '+relative)
    resource.setrlimit(resource.RLIMIT_AS, (512*1024*1024, 512*1024*1024))
    resource.setrlimit(resource.RLIMIT_FSIZE, (2*1024*1024, 2*1024*1024))
    resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
    signal.alarm(40)
    output.mkdir(mode=0o700)
    output = output.resolve()
    def permitted(path, write=False):
        candidate = Path(os.fsdecode(path)).absolute().resolve()
        return candidate == output or output in candidate.parents or (not write and (candidate == PACKET or PACKET in candidate.parents))
    def audit(event, values):
        if event.startswith('socket.') or event in ('subprocess.Popen', 'os.system', 'os.posix_spawn', 'os.fork', 'ctypes.dlopen'):
            raise PermissionError('network/native/process execution denied: '+event)
        if event == 'open' and not isinstance(values[0], int):
            path, mode, flags = values
            write = bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
            if not permitted(path, write): raise PermissionError('outside fixture file denied')
        if event in ('os.listdir', 'os.scandir') and values[0] is not None:
            if not permitted(values[0]): raise PermissionError('outside fixture directory denied')
        if event in ('os.mkdir', 'os.remove', 'os.rmdir', 'os.chmod', 'os.utime'):
            if not permitted(values[0], True): raise PermissionError('outside fixture mutation denied')
        if event in ('os.rename', 'os.link', 'os.symlink'):
            if not all(permitted(p, True) for p in values[:2]): raise PermissionError('outside fixture mutation denied')
        if event == 'sqlite3.connect':
            path = str(values[0]).removeprefix('file:').split('?', 1)[0]
            if not permitted(path, True): raise PermissionError('outside fixture database denied')
    sys.addaudithook(audit)
    for name, action in [('network', lambda: socket.socket()),
                         ('outside-read', lambda: Path('/etc/passwd').read_bytes()),
                         ('outside-write', lambda: (PACKET/'denied-write').write_text('must not exist'))]:
        try: action()
        except PermissionError: pass
        else: raise AssertionError('negative control failed: '+name)
    started = time.monotonic()
    result = {'evidence': 'synthetic source controls, not native hashing/offline gameplay',
              'identities': identities, 'python': sys.version, 'status': 'FAIL',
              'network_and_outside_path_negative_controls': 'PASS'}
    try:
        result['rvz'] = []
        check_rvz(result['rvz'])
        result['listing'] = []
        check_listing(output, result['listing'])
        result['status'] = 'PASS'
    except Exception as error:
        result['error'] = type(error).__name__ + ': ' + str(error)
        raise
    finally:
        result['elapsed_seconds'] = time.monotonic() - started
        result['fixture_bytes'] = sum(p.stat().st_size for p in output.rglob('*') if p.is_file())
        need(result['fixture_bytes'] <= 16*1024*1024, 'scratch allowance exceeded')
        (output/'result.json').write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps({'status': result['status'], 'result': str(output/'result.json')}))


if __name__ == '__main__':
    main()
