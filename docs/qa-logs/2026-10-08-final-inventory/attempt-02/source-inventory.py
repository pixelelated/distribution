#!/usr/bin/env python3
"""Read frozen inputs, unpack/build stamps and matching source-cache bytes (#383).

This is a post-build inventory, not a claim that every build-system fetch was
traced. Unmatched cache entries remain explicit for licence/source follow-up.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('checkout', type=Path)
p.add_argument('inputs', type=Path)
p.add_argument('output', type=Path)
a = p.parse_args()
m = json.loads(a.inputs.read_text())
root = a.checkout.resolve()
build = root / m['build_root']
cache = Path(m['source_cache'])


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def git(path, *args):
    return subprocess.check_output(['git', '-C', str(path), *args], text=True).strip()


assert git(root, 'rev-parse', 'HEAD') == m['distribution_commit']
for name, wanted in m['source_files'].items():
    assert sha(root / name) == wanted, name
print(f"PASS frozen commit and {len(m['source_files'])} source hashes", flush=True)
records = []
errors = []
recipes = {}
for fname in ('.cache_package_global', '.cache_package_local'):
    for line in (build / fname).read_text().splitlines():
        directory = Path(line.removesuffix('@?+?@'))
        recipes[directory.name] = str(directory.relative_to(m['container_worktree']) / 'package.mk')
def recipe(name):
    path = recipes[name]
    assert sha(root / path) == m['source_files'][path], path
    return path, (root / path).read_text()
custom = {'gamescope-glm', 'gamescope-stb', 'mangohud-vulkan-headers', 'mangohud-vulkan-utility-libraries'}

for d in sorted((build / 'build').iterdir()):
    identity = d / '.rocknix-package'
    if not identity.is_file():
        continue
    name = re.search(r'^INFO_PKG_NAME="([^"]+)"$', identity.read_text(), re.M)[1]
    record = {'package': name, 'unpacked': d.name, 'cache': [], 'build_stamps': {}}
    unpack = d / '.rocknix-unpack'
    record['unpack_stamp_sha256'] = sha(unpack) if unpack.exists() else None
    stamps = build / '.stamps' / name
    if stamps.exists():
        record['build_stamps'] = {f.name: sha(f) for f in sorted(stamps.glob('build_*'))}
    if (d / '.git').exists():
        # Some builds create an empty .git marker to suppress version probes;
        # rev-parse then walks up to the distribution repository. It is not
        # the package's provenance unless Git actually owns this source root.
        if Path(git(d, 'rev-parse', '--show-toplevel')).resolve() == d.resolve():
            record['unpacked_git_head'] = git(d, 'rev-parse', 'HEAD')
    cache_dir = cache / name
    special_name = None
    version = d.name[len(name) + 1:]
    if name in custom:
        path, text = recipe(name)
        source_name = re.search(r'^PKG_SOURCE_NAME="([^"\n]+)"$', text, re.M)[1]
        declared_version = re.search(r'^PKG_VERSION="([^"\n]+)"$', text, re.M)[1]
        assert declared_version == version, name
        special_name = source_name.replace('${PKG_VERSION}', version)
        assert '$' not in special_name and '/' not in special_name, special_name
    if name in ('cargo-snapshot' , 'rust-std-snapshot', 'rustc-snapshot'):
        special_name = f"{name}_{version}_{m['arch']}.tar.xz"
    elif name == 'noto-sans-cjk':
        special_name = f'NotoSansCJKsc-Regular-{version}.otf'
    if cache_dir.exists():
        for source in sorted(cache_dir.iterdir()):
            if source.name != special_name and source.name != d.name and not source.name.startswith(d.name + '.'):
                continue
            if source.name.endswith(('.url', '.sha256')):
                continue
            if name == 'simple-http-server' and f".{m['arch']}-" not in source.name:
                continue
            if source.is_dir() and (source / '.git').exists():
                if 'unpacked_git_head' not in record:
                    continue  # An old clone beside the archive was not unpacked.
                item = {'name': source.name, 'git_head': git(source, 'rev-parse', 'HEAD'),
                        'submodules': git(source, 'submodule', 'status', '--recursive').splitlines()}
                if 'unpacked_git_head' in record and record['unpacked_git_head'] != item['git_head']:
                    errors.append(name + ': cached/unpacked git identities differ')
            elif source.is_file():
                if 'unpacked_git_head' in record:
                    continue
                item = {'name': source.name, 'sha256': sha(source), 'bytes': source.stat().st_size}
                stamp = source.with_name(source.name + '.sha256')
                item['checksum_stamp_matches'] = stamp.exists() and stamp.read_text().strip() == item['sha256']
                if not item['checksum_stamp_matches']:
                    errors.append(name + ': archive checksum stamp differs/missing')
            else:
                continue
            if name in custom:
                wanted = re.search(r'^PKG_SHA256="([0-9a-f]{64})"$', recipe(name)[1], re.M)[1]
                assert item['sha256'] == wanted, name
                item['recipe_checksum_matches'] = True
            record['cache'].append(item)
    records.append(record)
    if len(records) % 50 == 0:
        print(f"inventory: {len(records)} unpacked packages recorded", flush=True)
by_name = {r['package']: r for r in records}
local = {'autostart', 'cloud-signin-window', 'control-gen', 'emulators', 'entware',
         'installer', 'mako-notify', 'modules', 'pico-8', 'powerstate', 'quirks',
         'rocknix', 'rocknix-screenshot', 'sdl2notify', 'sdl2text', 'sleep', 'system-utils'}
parents = {'cargo': ['cargo-snapshot', 'rust'], 'nspr': ['nss'], 'harfbuzz-icu': ['harfbuzz'], 'libclc': ['llvm']}
for record in records:
    name = record['package']
    if record['cache']:
        record['provenance'] = 'matching source-cache input; checksums/git identity verified'
    elif name in local:
        record['provenance'] = 'local/generated package; source inputs covered by frozen manifest'
    elif name in parents:
        record['provenance'] = 'shared source from unpack dependencies'
        record['source_packages'] = {p: by_name[p]['unpacked'] for p in parents[name]}
    elif name in ('device-tree-overlays', 'list-guid', 'heroic'):
        path, text = recipe(name)
        assert 'PKG_URL=' not in text or 'PKG_URL=""' in text, name
        source_dir = Path(path).parent
        covered = {p: h for p, h in m['source_files'].items() if p.startswith(str(source_dir) + '/')}
        assert len(covered) > 1, name
        record['provenance'] = 'local helper source/scripts covered by frozen product manifest'
        record['local_source_files'] = covered
        if name == 'heroic':
            record['scope_note'] = 'Runtime launcher scripts only; recipe metadata is not a licence assessment of externally user-installed Heroic software'
    elif name == 'lib32':
        path, text = recipe(name)
        assert m['arch'] == 'aarch64' and 'LIBARCH="arm"' in text and '${LIBROOT}/usr/lib/*' in text
        arm = root / ('build.pixelelated-' + m['device'] + '.arm')
        assert (arm / 'image/system/usr/lib').is_dir()
        record['provenance'] = 'generated compatibility bundle copied from same-target ARM image; companion ARM inventory and accepted handoff bind components'
        record['source_profile'] = m['device'] + '.arm'
        record['source_build_root'] = str(arm)
        record['recipe_sha256'] = sha(root / path)
    elif name == 'u-boot' and m['device'] == 'H700':
        path, text = recipe(name)
        assert 'PKG_DEPENDS_UNPACK+=" u-boot-${PKG_SUBDEVICE}"' in text
        source_names = [n for n in by_name if n.startswith('u-boot-')]
        assert set(source_names) == {'u-boot-DDR3', 'u-boot-DDR4'}, source_names
        assert all(by_name[n]['cache'] for n in source_names)
        record['provenance'] = 'local packaging of separately inventoried DDR3/DDR4 U-Boot outputs'
        record['source_packages'] = {n: by_name[n]['unpacked'] for n in source_names}
    elif name == 'idtech-lr':
        path, text = recipe(name)
        assert 'curl -Lo ${INSTALL}/usr/share/idtech/doom.tar.gz ${PKG_DOOM_SHAREWARE}' in text
        installed = build / 'image/system/usr/share/idtech/doom.tar.gz'
        staged = build / 'build' / record['unpacked'] / '.install_pkg/usr/share/idtech/doom.tar.gz'
        assert installed.is_file() and staged.is_file()
        assert sha(installed) == sha(staged)
        record['provenance'] = 'local launcher package plus install-time downloaded shareware asset'
        record['downloaded_asset'] = {'url': re.search(r'^PKG_DOOM_SHAREWARE="([^"\n]+)"$', text, re.M)[1], 'installed_path': str(installed), 'sha256': sha(installed), 'bytes': installed.stat().st_size, 'staged_bytes_match': True, 'disposition': 'HOLD: unpinned install-time download; exact bytes retained, upstream provenance and redistribution notice review remain'}
    elif name == 'rclone':
        rclone_arch = 'arm64' if m['arch'] == 'aarch64' else 'amd64'
        binary = build / 'build' / record['unpacked'] / ('rclone-v1.75.1-linux-' + rclone_arch) / 'rclone'
        record['provenance'] = 'prebuilt binary; recipe deletes the downloaded ZIP after unpack'
        record['unpacked_binary_sha256'] = sha(binary)
        record['archive_retention'] = 'ZIP absent; reconstruct/retain before publication source custody is complete'
    else:
        record['provenance'] = 'UNCLASSIFIED'
        errors.append(name + ': source provenance unclassified')
result = {'schema': 1, 'input_manifest_sha256': sha(a.inputs),
          'distribution_commit': m['distribution_commit'], 'records': records,
          'unmatched_cache_packages': [r['package'] for r in records if not r['cache']],
          'errors': errors}
a.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
print(f"inventory: {len(records)} source roots; {sum(len(r['cache']) for r in records)} cache inputs; "
      f"{len(result['unmatched_cache_packages'])} without a default-name cache match; {len(errors)} errors", flush=True)
for name in ('emulationstation', 'raofflineproxy', 'webkitgtk', 'libsoup', 'glslang', 'spirv-headers', 'cbindgen', 'tllist'):
    found = [r['unpacked'] for r in records if r['package'] == name]
    print(name + ': ' + ', '.join(found), flush=True)
if errors:
    raise SystemExit('\n'.join(errors))
