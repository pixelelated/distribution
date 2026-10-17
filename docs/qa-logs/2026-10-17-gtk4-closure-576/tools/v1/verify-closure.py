#!/usr/bin/env python3
"""Read-only post-build inventory; readelf only, never ldd or target execution."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import time

COMMIT = '969354955741d6c0ca8ce816e1c59ad338b1605b'
BUILD = 'build.pixelelated-GENERIC_X64.x86_64'
TRIPLE = 'x86_64-rocknix-linux-gnu'
CANONICAL = Path('/workspace/repos/rocknix.worktrees/m7-pixelelated')
VERSIONS = {'webkitgtk': '2.54.1', 'gtk4': '4.24.1', 'graphene': '1.10.8',
            'libseccomp': '2.6.1', 'bubblewrap': '0.11.2', 'xdg-dbus-proxy': '0.1.7'}
REQUIRED = {
    'webkitgtk': ['/usr/lib/libwebkitgtk-6.0.so', '/usr/lib/libjavascriptcoregtk-6.0.so',
                  '/usr/libexec/webkitgtk-6.0/WebKitWebProcess',
                  '/usr/libexec/webkitgtk-6.0/WebKitNetworkProcess',
                  '/usr/lib/webkitgtk-6.0/injected-bundle/libwebkitgtkinjectedbundle.so'],
    'gtk4': ['/usr/lib/libgtk-4.so.1'], 'graphene': ['/usr/lib/libgraphene-1.0.so.0'],
    'libseccomp': ['/usr/lib/libseccomp.so.2'], 'bubblewrap': ['/usr/bin/bwrap'],
    'xdg-dbus-proxy': ['/usr/bin/xdg-dbus-proxy']}
PC = {'webkitgtk': ['webkitgtk-6.0.pc', 'javascriptcoregtk-6.0.pc'],
      'gtk4': ['gtk4.pc'], 'graphene': ['graphene-1.0.pc', 'graphene-gobject-1.0.pc'],
      'libseccomp': ['libseccomp.pc']}
DEFAULT_DIRS = ['/lib64', '/usr/lib64', '/lib', '/usr/lib',
                '/lib/x86_64-linux-gnu', '/usr/lib/x86_64-linux-gnu']


def norm(path):
    parts = []
    for part in PurePosixPath(path).parts:
        if part in ('/', '.', ''):
            continue
        if part == '..':
            if not parts:
                raise ValueError('path escapes virtual root: ' + path)
            parts.pop()
        else:
            parts.append(part)
    return '/' + '/'.join(parts)


class Verifier:
    def __init__(self, args):
        self.args = args
        self.started = time.monotonic()
        self.build = args.checkout / BUILD
        self.sysroot = self.build / 'toolchain' / TRIPLE / 'sysroot'
        self.baseline = args.baseline_build / 'toolchain' / TRIPLE / 'sysroot'
        self.prefixes = [str(CANONICAL / BUILD / 'toolchain' / TRIPLE / 'sysroot'),
                         str(self.sysroot), str(self.baseline)]
        self.layers = [('package:' + name, self.build / 'install_pkg' / (name + '-' + version))
                       for name, version in VERSIONS.items()]
        self.layers += [('isolated-sysroot', self.sysroot), ('accepted-baseline-fallback', self.baseline)]
        self.hashes, self.elfs = {}, {}
        self.report = {'status': 'FAIL', 'read_only': True, 'target_code_executed': False,
                       'source_commit': COMMIT, 'versions': VERSIONS, 'errors': [], 'stamps': {},
                       'critical_artifacts': [], 'closure': [], 'edges': [], 'baseline_fallbacks': [],
                       'limitations': ['ELF NEEDED/interpreter closure only; not symbol-version ABI, dlopen, GTK/GIO/GStreamer modules, schemas, fonts, or certificates.',
                                       'No ld.so.cache/hwcaps, LD_LIBRARY_PATH, or platform-dependent $LIB expansion is modeled.',
                                       'A closure PASS is not a loader, input, rendering, performance, or sandbox-isolation PASS.']}

    def bound(self):
        if time.monotonic() - self.started > self.args.seconds:
            raise TimeoutError('read-only verification deadline exceeded')

    def sha(self, path):
        self.bound()
        before = path.stat()
        key = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        if key not in self.hashes:
            digest = hashlib.sha256()
            with path.open('rb') as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    self.bound()
                    digest.update(block)
            after = path.stat()
            if key != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
                raise ValueError('artifact changed during read: ' + str(path))
            self.hashes[key] = digest.hexdigest()
        return self.hashes[key]

    def resolve(self, root, virtual):
        """Resolve links inside one virtual target root, never host absolute links."""
        current = norm(virtual)
        links = []
        for _ in range(41):
            parts = PurePosixPath(current).parts[1:]
            for i in range(len(parts)):
                local = root.joinpath(*parts[:i + 1])
                try:
                    st = local.lstat()
                except FileNotFoundError:
                    return None
                if stat.S_ISLNK(st.st_mode):
                    target = os.readlink(local)
                    links.append({'at': '/' + '/'.join(parts[:i + 1]), 'target': target})
                    for prefix in self.prefixes:
                        if target == prefix or target.startswith(prefix + '/'):
                            target = target[len(prefix):] or '/'
                            break
                    if target.startswith('/workspace/'):
                        raise ValueError('unmapped build-root symlink: ' + target)
                    if not target.startswith('/'):
                        target = '/' + '/'.join(parts[:i]) + '/' + target
                    current = norm(target + '/' + '/'.join(parts[i + 1:]))
                    break
            else:
                path = root.joinpath(*parts)
                return {'path': path, 'virtual': current, 'links': links} if path.is_file() else None
        raise ValueError('symlink loop: ' + virtual)

    def elf(self, path):
        self.bound()
        digest = self.sha(path)
        if digest in self.elfs:
            return self.elfs[digest]
        with path.open('rb') as stream:
            if stream.read(4) != b'\x7fELF':
                raise ValueError('not ELF: ' + str(path))
        proc = subprocess.run([self.args.readelf, '-W', '-h', '-l', '-d', '-n', str(path)],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                              timeout=min(15, max(1, self.args.seconds - (time.monotonic() - self.started))),
                              env=dict(os.environ, LC_ALL='C'))
        if proc.returncode:
            raise ValueError('readelf failed: ' + str(path) + ': ' + proc.stderr[:600])
        def field(pattern):
            match = re.search(pattern, proc.stdout, re.M)
            return match.group(1).strip() if match else None
        data = {'sha256': digest, 'bytes': path.stat().st_size,
                'machine': field(r'^\s*Machine:\s*(.+)$'), 'class': field(r'^\s*Class:\s*(.+)$'),
                'type': field(r'^\s*Type:\s*(\S+)'), 'build_id': field(r'Build ID:\s*(\S+)'),
                'interpreter': field(r'\[Requesting program interpreter:\s*(.*?)\]'),
                'soname': field(r'\(SONAME\).*?\[(.*?)\]'),
                'needed': re.findall(r'\(NEEDED\).*?\[(.*?)\]', proc.stdout),
                'rpath': field(r'\(RPATH\).*?\[(.*?)\]'),
                'runpath': field(r'\(RUNPATH\).*?\[(.*?)\]')}
        if data['class'] != 'ELF64' or data['machine'] != 'Advanced Micro Devices X86-64':
            raise ValueError('unexpected target ELF architecture: ' + str(path))
        self.elfs[digest] = data
        return data

    def choose(self, virtual_paths):
        for virtual in virtual_paths:
            for label, root in self.layers:
                found = self.resolve(root, virtual)
                if found:
                    found.update(layer=label, requested=virtual)
                    return found
        return None

    def run(self):
        head = subprocess.check_output(['git', '-C', str(self.args.checkout), 'rev-parse', 'HEAD'],
                                       text=True, timeout=10).strip()
        if head != COMMIT:
            raise ValueError('checkout commit mismatch: ' + head)
        cache_path = self.build / 'build/webkitgtk-2.54.1/.x86_64-rocknix-linux-gnu/CMakeCache.txt'
        cache = dict(re.findall(r'^([^#/:][^:=]*):[^=]*=(.*)$', cache_path.read_text(), re.M))
        expected = {'PORT': 'GTK', 'CMAKE_BUILD_TYPE': 'Release', 'USE_GTK4': 'ON',
                    'ENABLE_BUBBLEWRAP_SANDBOX': 'ON', 'ENABLE_WAYLAND_TARGET': 'ON',
                    'USE_SKIA': 'ON', 'USE_GBM': 'ON', 'BWRAP_EXECUTABLE': '/usr/bin/bwrap',
                    'DBUS_PROXY_EXECUTABLE': '/usr/bin/xdg-dbus-proxy',
                    'LIBEXEC_INSTALL_DIR': '/usr/libexec/webkitgtk-6.0'}
        self.report['configuration'] = {key: cache.get(key) for key in expected}
        for key, value in expected.items():
            if cache.get(key) != value:
                raise ValueError('CMake configuration mismatch: ' + key)
        required = {name: list(paths) for name, paths in REQUIRED.items()}
        if cache.get('ENABLE_GPU_PROCESS') == 'ON':
            required['webkitgtk'].append('/usr/libexec/webkitgtk-6.0/WebKitGPUProcess')
        seeds = []
        for name, version in VERSIONS.items():
            stamp = self.build / '.stamps' / name / 'build_target'
            stamp_text = stamp.read_text()
            if 'STAMP_PKG_NAME="' + name + '"' not in stamp_text or 'STAMP_BUILD_WITH_DEBUG="no"' not in stamp_text:
                raise ValueError('missing/unexpected completed package stamp: ' + name)
            self.report['stamps'][name] = {'sha256': self.sha(stamp), 'text': stamp_text}
            package = self.build / 'install_pkg' / (name + '-' + version)
            for filename in PC.get(name, []):
                for root in [package, self.sysroot]:
                    pc = self.resolve(root, '/usr/lib/pkgconfig/' + filename)
                    if not pc or not re.search(r'^Version:\s*' + re.escape(version) + r'\s*$', pc['path'].read_text(), re.M):
                        raise ValueError('missing/version-mismatched pkg-config: ' + str(root / filename))
            for virtual in required[name]:
                pair = []
                for label, root in [('package:' + name, package), ('isolated-sysroot', self.sysroot)]:
                    found = self.resolve(root, virtual)
                    if not found:
                        raise ValueError('missing critical artifact: ' + label + ':' + virtual)
                    found.update(layer=label, requested=virtual)
                    data = self.elf(found['path'])
                    if '/bin/' in virtual or '/libexec/' in virtual:
                        if not found['path'].stat().st_mode & 0o111 or not data['interpreter']:
                            raise ValueError('non-executable/missing interpreter: ' + virtual)
                    pair.append((found, data))
                    seeds.append((found, []))
                left, right = pair[0][1], pair[1][1]
                fields = ['machine', 'class', 'type', 'interpreter', 'soname', 'needed', 'rpath', 'runpath']
                same_identity = all(left[key] == right[key] for key in fields)
                same_build = bool(left['build_id']) and left['build_id'] == right['build_id']
                if not same_identity or not (same_build or left['sha256'] == right['sha256']):
                    raise ValueError('package/sysroot attribution mismatch: ' + virtual)
                self.report['critical_artifacts'].append({'package': name, 'virtual': virtual,
                    'package_elf': left, 'sysroot_elf': right, 'matching_build_id': same_build,
                    'bytes_identical': left['sha256'] == right['sha256']})
        for path in self.args.extra_elf:
            seeds.append(({'path': path, 'virtual': '/tmp/' + path.name, 'requested': '/tmp/' + path.name,
                           'links': [], 'layer': 'extra-elf'}, []))
        seen = set()
        while seeds:
            self.bound()
            found, inherited_rpath = seeds.pop(0)
            key = (str(found['path']), tuple(inherited_rpath))
            if key in seen:
                continue
            seen.add(key)
            if len(seen) > self.args.max_nodes:
                raise ValueError('ELF closure node limit reached')
            data = self.elf(found['path'])
            origin = str(PurePosixPath(found['virtual']).parent)
            search = []
            for entry in (data['runpath'] or data['rpath'] or '').split(':'):
                if not entry:
                    continue
                entry = entry.replace('${ORIGIN}', origin).replace('$ORIGIN', origin)
                if '$' in entry or not entry.startswith('/') or entry.startswith('/workspace/'):
                    raise ValueError('unsupported/runtime-invalid ELF search path: ' + entry)
                search.append(norm(entry))
            child_rpath = list(dict.fromkeys(inherited_rpath if data['runpath'] else search + inherited_rpath))
            search = list(dict.fromkeys(search + inherited_rpath + DEFAULT_DIRS))
            baseline = self.resolve(self.baseline, found['requested'])
            inherited = bool(baseline) and self.sha(baseline['path']) == data['sha256']
            node = {'path': str(found['path']), 'runtime_path': found['requested'], 'resolved_virtual': found['virtual'],
                    'layer': found['layer'], 'inherited_bytes': inherited, 'links': found['links'], 'elf': data}
            self.report['closure'].append(node)
            if found['layer'] == 'accepted-baseline-fallback':
                self.report['baseline_fallbacks'].append(found['requested'])
            dependencies = [('needed', name) for name in data['needed']]
            if data['interpreter']:
                dependencies.append(('interpreter', data['interpreter']))
            for kind, name in dependencies:
                if '/' in name:
                    if not name.startswith('/'):
                        raise ValueError('relative slash in ELF dependency: ' + name)
                    candidates = [norm(name)]
                else:
                    candidates = [norm(directory + '/' + name) for directory in search]
                child = self.choose(candidates)
                edge = {'from': str(found['path']), 'kind': kind, 'name': name,
                        'resolved_layer': child['layer'] if child else None,
                        'resolved_path': str(child['path']) if child else None}
                self.report['edges'].append(edge)
                if child:
                    seeds.append((child, child_rpath))
                else:
                    self.report['errors'].append('missing ' + kind + ': ' + name + ' from ' + str(found['path']))
        for name, previous in self.report['stamps'].items():
            if self.sha(self.build / '.stamps' / name / 'build_target') != previous['sha256']:
                raise ValueError('package stamp changed during verification: ' + name)
        if not self.report['errors']:
            self.report['status'] = 'PASS_WITH_BASELINE_FALLBACK' if self.report['baseline_fallbacks'] else 'PASS'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout', type=Path, default=Path('/workspace/repos/rocknix.worktrees/m7-gtk4-build-20261017-01'))
    parser.add_argument('--baseline-build', type=Path, default=Path('/workspace/repos/rocknix.worktrees/m7-p5-build-20261015-03') / BUILD)
    parser.add_argument('--readelf', default='/usr/bin/readelf')
    parser.add_argument('--seconds', type=int, default=180, choices=range(1, 601))
    parser.add_argument('--max-nodes', type=int, default=512, choices=range(1, 2049))
    parser.add_argument('--extra-elf', type=Path, action='append', default=[])
    args = parser.parse_args()
    verifier = Verifier(args)
    try:
        verifier.run()
    except Exception as error:
        verifier.report['errors'].append(type(error).__name__ + ': ' + str(error))
    verifier.report['elapsed_seconds'] = time.monotonic() - verifier.started
    print(json.dumps(verifier.report, indent=2))
    return 0 if verifier.report['status'].startswith('PASS') else 1


if __name__ == '__main__':
    raise SystemExit(main())
