"""Build 28's independent SM8550 raw/update acceptance (#555's SM8550 checkbox): GPT, raw and update
SYSTEM/KERNEL equality, OpenABL 1.2's files in the tar, the SYSTEM and the boot partition, os-release, userland
architecture, the ARM handoff (retroarch32, box86, two 32-bit cores and every usr/lib32 library) and FEX.
Read-only on the build's outputs; its scratch is removed. Modelled on the 2026-10-11 verify-firmware.py,
adjusted to OpenABL's folder (openabl/, which replaced rocknix_abl/). Exit 0 PASS, 1 a FAIL, 2 could not run."""
import gzip, hashlib, json, os, shutil, subprocess, sys, tarfile
from pathlib import Path

WT = Path('/workspace/repos/rocknix.worktrees/m7-round-sm8550-20261128')
HEAD = '6169621a4b93630c20dc6cd642b7983a2f3a2c44'
BRANCH = 'build/m7-round-sm8550-20261128'
OUT = Path(sys.argv[1])
SCRATCH = Path('/workspace/tmp/rocknix-session/build28-raw-scratch')
ARM = WT / 'build.pixelelated-SM8550.arm/image/system'
MTOOLS = WT / 'build.pixelelated-SM8550.aarch64/toolchain/bin'
import datetime
RUN_START = datetime.datetime.fromisoformat(
    (WT / '.build-runs/20261128T064843Z-a7b15e8b/build.start').read_text().strip()).timestamp()
fails, rec = [], {}


def check(ok, what):
    print(('PASS ' if ok else 'FAIL ') + what, flush=True)
    if not ok:
        fails.append(what)
    return ok


def digest(path):
    with open(path, 'rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def cat(system, name):
    r = subprocess.run(['unsquashfs', '-cat', str(system), name], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def elf(b):
    if not b or b[:4] != b'\x7fELF':
        return None
    return {1: 'ELF32', 2: 'ELF64'}.get(b[4]), {1: 'LE', 2: 'BE'}.get(b[5]), int.from_bytes(b[18:20], 'little')


if SCRATCH.exists():
    shutil.rmtree(SCRATCH)
SCRATCH.mkdir(parents=True)
try:
    tgt = WT / 'target'
    img = [p for p in tgt.glob(f'*.g{HEAD[:12]}*.img.gz')]
    tar = [p for p in tgt.glob(f'*.g{HEAD[:12]}*.tar')]
    if len(img) != 1 or len(tar) != 1:
        print(f'cannot run: {len(img)} images and {len(tar)} tars at {HEAD[:12]}'); sys.exit(2)
    img, tar = img[0], tar[0]
    rec['image'], rec['tar'] = img.name, tar.name
    for p in (img, tar):
        want, name = (p.parent / (p.name + '.sha256')).read_text().split()
        got = digest(p)
        rec[p.name] = got
        check(Path(name).name == p.name and got == want, f'{p.name} sha256 {got} matches its .sha256')

    # The update tar: SYSTEM, KERNEL and the boot files under 3rdparty/bootloader/.
    system = SCRATCH / 'SYSTEM'
    boot = {}
    with tarfile.open(tar) as tf:
        m = tf.getnames()
        sysn = [n for n in m if n.endswith('/target/SYSTEM')]
        kern = [n for n in m if n.endswith('/target/KERNEL')]
        if len(sysn) != 1 or len(kern) != 1:
            print('cannot run: the tar lacks one SYSTEM and one KERNEL'); sys.exit(2)
        with tf.extractfile(sysn[0]) as s, system.open('xb') as d:
            shutil.copyfileobj(s, d, 4 << 20)
        with tf.extractfile(kern[0]) as s:
            kernel_hash = hashlib.file_digest(s, 'sha256').hexdigest()
        for mem in tf.getmembers():
            if mem.isfile() and '/3rdparty/bootloader/' in mem.name:
                rel = mem.name.split('/3rdparty/bootloader/', 1)[1]
                with tf.extractfile(mem) as s:
                    data = s.read()
                boot[rel] = (hashlib.sha256(data).hexdigest(), elf(data) if rel.endswith('.elf') else None)
    system_hash = digest(system)
    rec['system_sha256'], rec['kernel_sha256'] = system_hash, kernel_hash
    print(f'update tar: SYSTEM {system_hash}, KERNEL {kernel_hash}, {len(boot)} boot files')

    # OpenABL 1.2: the signed ABL is ELF32/LE/EM_ARM (40), as #602 recorded; its folder matches the SYSTEM's copy.
    abl = boot.get('openabl/abl_signed-SM8550.elf')
    check(abl is not None, 'the tar carries 3rdparty/bootloader/openabl/abl_signed-SM8550.elf')
    if abl:
        check(abl[1] == ('ELF32', 'LE', 40), f'the signed ABL is ELF32/LE/EM_ARM: {abl[1]}, sha256 {abl[0]}')
    openabl = {k: v[0] for k, v in boot.items() if k.startswith('openabl/')}
    rec['openabl'] = openabl
    for rel, sha in sorted(openabl.items()):
        b = cat(system, 'usr/share/bootloader/' + rel)
        check(b is not None and hashlib.sha256(b).hexdigest() == sha, f'SYSTEM usr/share/bootloader/{rel} equals the tar\'s ({sha[:16]})')

    # os-release.
    rel = (cat(system, 'etc/os-release') or b'').decode()
    v = {k: x.strip('"') for k, x in (l.split('=', 1) for l in rel.splitlines() if '=' in l)}
    rec['os_release'] = {k: v.get(k) for k in ('OS_NAME', 'OS_VERSION', 'BUILD_DIRTY', 'BUILD_ID', 'BUILD_BRANCH', 'BUILD_VERSION', 'HW_DEVICE', 'HW_ARCH')}
    for k, want in dict(OS_NAME='pixelelated', OS_VERSION='0.0.1-dev', BUILD_DIRTY='no', BUILD_ID=HEAD, BUILD_BRANCH=BRANCH,
                        HW_DEVICE='SM8550', HW_ARCH='aarch64').items():
        check(v.get(k) == want, f'os-release {k}={v.get(k)!r}')
    check(v.get('BUILD_VERSION', '').endswith('.g' + HEAD[:12]), f'os-release BUILD_VERSION {v.get("BUILD_VERSION")!r} names the head')
    ident = json.loads(next(tgt.glob(f'*.g{HEAD[:12]}*.identity.json')).read_text())
    check(ident.get('build_commit') == HEAD and ident.get('build_version') == v.get('BUILD_VERSION'), 'identity.json names the head and the version')

    # Userland architecture.
    for name in ('usr/bin/emulationstation', 'usr/bin/retroarch', 'usr/bin/FEX'):
        e = elf(cat(system, name))
        check(e == ('ELF64', 'LE', 183), f'{name} is ELF64/LE/AArch64: {e}')

    # The ARM handoff, against this run's ARM image (built 06:48 onward).
    arm_t = (ARM / 'usr/bin/retroarch').stat().st_mtime
    check(arm_t > RUN_START, 'the ARM image was written by this run')
    handoff = []
    for src, dst in {'usr/bin/retroarch': 'usr/bin/retroarch32', 'usr/bin/box86': 'usr/bin/box86',
                     'usr/lib/libretro/gpsp_libretro.so': 'usr/lib/libretro/gpsp_libretro.so',
                     'usr/lib/libretro/desmume_libretro.so': 'usr/lib/libretro/desmume_libretro.so'}.items():
        b = cat(system, dst)
        a = (ARM / src).read_bytes() if (ARM / src).is_file() else None
        ok = b is not None and a is not None and elf(b) == ('ELF32', 'LE', 40) and hashlib.sha256(b).digest() == hashlib.sha256(a).digest()
        check(ok, f'{dst} is ELF32/LE/ARM and equals the ARM image\'s {src}')
        handoff.append({'source': src, 'installed': dst, 'sha256': hashlib.sha256(b).hexdigest() if b else None})
    # lib32: rsync -al of the ARM image's usr/lib/* (projects/ROCKNIX/packages/compat/lib32), so each top-level regular file.
    libs = sorted(p for p in (ARM / 'usr/lib').iterdir() if p.is_file() and not p.is_symlink())
    listing = subprocess.check_output(['unsquashfs', '-ll', str(system), 'usr/lib32'], text=True)
    same, differ = 0, []
    for p in libs:
        b = cat(system, 'usr/lib32/' + p.name)
        if b is not None and hashlib.sha256(b).digest() == hashlib.sha256(p.read_bytes()).digest():
            same += 1
        else:
            differ.append(p.name)
    check(libs and not differ, f'usr/lib32 carries the ARM image\'s {len(libs)} top-level usr/lib files byte for byte ({same} equal; differ: {differ[:8]})')
    rec['arm_handoff'] = {'files': handoff, 'lib32_equal': same, 'lib32_differ': differ}

    # FEX: the interpreter, both binfmt confs, the guest thunks.
    fl = subprocess.check_output(['unsquashfs', '-l', str(system)], text=True).splitlines()
    fex = [l.split('squashfs-root/', 1)[1] for l in fl if 'fex' in l.lower() and 'squashfs-root/' in l]
    rec['fex_entries'] = len(fex)
    for need in ('usr/bin/FEX', 'usr/lib/binfmt.d/FEX-x86.conf', 'usr/lib/binfmt.d/FEX-x86_64.conf'):
        check(need in fex, f'the SYSTEM lists {need}')
    thunks = [x for x in fex if x.startswith('usr/share/fex-emu/GuestThunks/')]
    check(len(thunks) > 0, f'{len(thunks)} files under usr/share/fex-emu/GuestThunks')

    # The raw image: GPT, then the boot partition's SYSTEM, KERNEL and boot files against the tar's.
    raw = SCRATCH / 'SM8550.img'
    with gzip.open(img, 'rb') as s, raw.open('xb') as d:
        while block := s.read(4 << 20):
            if block.count(0) == len(block):
                d.seek(len(block), 1)
            else:
                d.write(block)
        d.truncate()
    rec['raw_bytes'], rec['raw_sha256'] = raw.stat().st_size, digest(raw)
    pt = json.loads(subprocess.check_output(['/usr/sbin/sfdisk', '--json', str(raw)], text=True))['partitiontable']
    rec['partition_table'] = pt
    parts = pt.get('partitions', [])
    check(pt.get('label') == 'gpt' and pt.get('sectorsize') == 512, f'the raw image has a GPT with 512-byte sectors ({pt.get("label")}, {pt.get("sectorsize")})')
    check([p.get('name') for p in parts] == ['system', 'storage'], f'its partitions are system, storage: {[(p.get("name"), p.get("start"), p.get("size")) for p in parts]}')
    first = parts[0]['start'] if parts else 0
    check(first >= 2048, f'the system partition starts at sector {first}')
    env = dict(os.environ, MTOOLS_SKIP_CHECK='1')
    at = f'{raw}@@{first * 512}'
    fat = subprocess.run([str(MTOOLS / 'mdir'), '-i', at, '-/', '-b', '::/'], capture_output=True, text=True, env=env)
    fat_files = sorted(l.removeprefix('::/') for l in fat.stdout.split() if l.startswith('::/'))
    rec['boot_partition_files'] = fat_files
    print(f'boot partition: {len(fat_files)} files, mdir rc {fat.returncode}')
    if not check(fat.returncode == 0 and fat_files, 'the boot partition can be listed'):
        raise SystemExit
    for name, want in (('SYSTEM', system_hash), ('KERNEL', kernel_hash)):
        out = SCRATCH / ('raw-' + name)
        r = subprocess.run([str(MTOOLS / 'mcopy'), '-i', at, '::/' + name, str(out)], capture_output=True, env=env)
        check(r.returncode == 0 and digest(out) == want, f'the raw image\'s {name} equals the update tar\'s')
        out.unlink(missing_ok=True)
    on_both = [k for k in boot if k in fat_files]
    rec['boot_files_on_both'] = on_both
    for k in sorted(on_both):
        out = SCRATCH / 'raw-boot'
        r = subprocess.run([str(MTOOLS / 'mcopy'), '-i', at, '::/' + k, str(out)], capture_output=True, env=env)
        check(r.returncode == 0 and digest(out) == boot[k][0], f'the boot partition\'s {k} equals the tar\'s')
        out.unlink(missing_ok=True)
    check('openabl/abl_signed-SM8550.elf' in on_both, 'the boot partition carries openabl/abl_signed-SM8550.elf')
    only_tar = sorted(k for k in boot if k not in fat_files)
    rec['boot_files_only_in_tar'] = only_tar
    print(f'boot files in the tar and not on the boot partition: {only_tar}')
finally:
    shutil.rmtree(SCRATCH, ignore_errors=True)
    rec['fails'] = fails
    OUT.write_text(json.dumps(rec, indent=1) + '\n')
print('== ' + ('PASS: build 28 raw/update acceptance' if not fails else f'FAIL: {len(fails)} checks'))
sys.exit(1 if fails else 0)
