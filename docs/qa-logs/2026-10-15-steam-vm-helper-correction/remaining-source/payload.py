"""Synthetic data generators. Imported only by a later allocated VM fixture."""
import io
import hashlib
import json
from pathlib import Path
import tarfile
import zipfile

RUNTIME = 'steam-runtime-steamrt-arm64'
CACHY = 'proton-cachyos-qa-arm64'
GE = 'GE-Protonqa-aarch64'
LIBS = ('libibus-1.0.so.5', 'libva.so.2')
STEAM = Path('/storage/.local/share/Steam')
ALIAS_TARGET = Path('/storage/games-internal/roms/steam')


def elf(machine=183, kind=3, label=b'synthetic-only'):
    header = bytearray(64)
    header[:6] = b'\x7fELF\x02\x01'
    header[16:18] = kind.to_bytes(2, 'little')
    header[18:20] = machine.to_bytes(2, 'little')
    return bytes(header) + label


def put(path, data, mode=0o644):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data.encode() if isinstance(data, str) else data)
    path.chmod(mode)


def proton_files(name):
    return {
        'toolmanifest.vdf': (b'"manifest" { "version" "2" "commandline" "/proton %verb%" }', 0o644),
        'compatibilitytool.vdf': (('"compatibilitytools" { "compat_tools" { "' + name +
                                  '" { "install_path" "." "from_oslist" "windows" "to_oslist" "linux" } } }').encode(), 0o644),
        'proton': (b'#!/bin/sh\nexit 91\n', 0o755),
        'filelock.py': (b'# synthetic structural input, never imported\n', 0o644),
        'version': (name.encode(), 0o644),
        'files/bin-arm64/wine': (elf(kind=2), 0o755),
        'files/bin-arm64/wineserver': (elf(kind=2), 0o755),
    }


def archive(path, prefix, files, mode):
    with tarfile.open(path, mode, format=tarfile.PAX_FORMAT) as bundle:
        for name, (data, permissions) in sorted(files.items()):
            member = tarfile.TarInfo(prefix + '/' + name)
            member.size, member.mode, member.mtime = len(data), permissions, 0
            bundle.addfile(member, io.BytesIO(data))
    assert path.stat().st_size <= 1024**2


def fex_tree(root, label):
    for name in ('usr/bin/env', 'usr/lib/ld-linux-x86-64.so.2', 'usr/lib/libc.so.6'):
        put(root / name, elf(62, label=label.encode()), 0o755)
    put(root / 'graphics_provider.json', '{"synthetic":true}')
    put(root / 'usr/share/vulkan/icd.d/freedreno_icd.x86_64.json',
        '{"ICD":{"library_path":"/usr/lib/libvulkan_freedreno.so"}}')
    (root / 'usr/share/vulkan/implicit_layer.d').mkdir(parents=True)
    put(root / 'synthetic-generation', label)


def original_case_root(case):
    assert case in ('fresh-client-real-root', 'existing-internal-alias')
    return ALIAS_TARGET if case == 'existing-internal-alias' else STEAM


def build(output, packet, installer, case):
    assert case in ('fresh-client-real-root', 'existing-internal-alias')
    jail, storage, qa = output / 'rootfs', output / 'storage', output / 'qa'
    for path in (storage, qa, output / 'tmp', jail):
        path.mkdir()
    for path in ('usr/bin', 'usr/lib', 'usr/config/modules', 'usr/share', 'bin', 'etc',
                 'system', 'storage', 'qa', 'tmp', 'proc', 'dev', 'run', 'var/media'):
        (jail / path).mkdir(parents=True, exist_ok=True)
    for name in ('payload.py', 'boundary.py', 'event_records.py'):
        put(qa / name, (packet / name).read_bytes())
    put(qa / 'events.ndjson', '')
    (qa / 'boundary-events').mkdir(mode=0o700)
    (qa / 'payloads').mkdir()
    put(qa / 'case.json', json.dumps({'name': case, 'physical_root': str(original_case_root(case)), 'steam': str(STEAM)}))
    files = {'steamrt3c_platform_qa/files/lib/aarch64-linux-gnu/' + name + '.qa':
             (elf(label=b'new-runtime'), 0o644) for name in LIBS}
    archive(qa / 'payloads/runtime.tar.xz', RUNTIME, files, 'w:xz')
    archive(qa / 'payloads/cachy.tar.xz', CACHY, proton_files(CACHY), 'w:xz')
    archive(qa / 'payloads/ge.tar.gz', GE, proton_files(GE), 'w:gz')
    put(jail / 'usr/config/modules/Install Steam.sh', installer, 0o755)
    put(jail / 'usr/config/fex-emu/Config.json', (packet / 'packaged/Config.json').read_bytes())
    put(jail / 'usr/config/fex-emu/AppConfig/steamwebhelper.json', (packet / 'packaged/steamwebhelper.json').read_bytes())
    put(jail / 'usr/lib/liblsfg-vk-layer.so', elf())
    put(jail / 'usr/share/fex-emu/liblsfg-vk-layer-x86.so', elf(62))
    for path, suffix in (('usr/share/vulkan/implicit_layer.d/VkLayer_LSFGVK_frame_generation.json', ''),
                         ('usr/share/fex-emu/VkLayer_LSFGVK_frame_generation-x86.json', '-x86')):
        put(jail / path, json.dumps({'layer': {'name': 'VK_LAYER_LSFGVK_frame_generation',
                        'library_path': '/usr/lib/liblsfg-vk-layer' + suffix + '.so'}}))
    put(jail / 'usr/share/steam/registry.vdf', '"Registry" { "synthetic" "only" }\n')
    put(jail / 'etc/profile', 'export PATH=/usr/bin:/bin\nset_kill() { /usr/bin/python3 -I -S -B /qa/boundary.py set_kill "$@"; }\n')
    for command in ('curl', 'wget', 'unzip', 'FEXRootFSFetcher', 'systemctl', 'swaymsg'):
        put(jail / 'usr/bin' / command,
            '#!/bin/sh\nexec /usr/bin/python3 -I -S -B /qa/boundary.py ' + command + ' "$@"\n', 0o755)
    steam = storage / original_case_root(case).relative_to('/storage')
    steam.mkdir(parents=True)
    if case == 'existing-internal-alias':
        alias = storage / STEAM.relative_to('/storage')
        alias.parent.mkdir(parents=True, exist_ok=True)
        alias.symlink_to(str(ALIAS_TARGET))
    for name in ('steamapps', 'userdata', 'depotcache'):
        put(steam / name / 'preserve', 'synthetic-' + name)
    put(storage / 'games-internal/roms/steam/unrelated', 'existing unused default library')
    put(storage / 'games-internal/roms/other-library/preserve', 'unrelated internal library')
    put(storage / 'games-external/untouched', 'no external mount selected')
    put(storage / '.steam/fixture-existing', 'existing support directory')
    for name in LIBS:
        target = 'steamrt3c_platform_old/files/lib/aarch64-linux-gnu/' + name + '.old'
        put(steam / RUNTIME / target, elf(label=b'old-runtime'))
        (steam / 'lib/aarch64-linux-gnu').mkdir(parents=True, exist_ok=True)
        (steam / 'lib/aarch64-linux-gnu' / name).symlink_to(str(STEAM / RUNTIME / target))
    for family in ('proton-cachyos-old-arm64', 'GE-Protonold-aarch64'):
        for name, (data, mode) in proton_files(family).items():
            put(steam / 'compatibilitytools.d' / family / name, data, mode)
    fex_tree(storage / '.local/share/fex-emu/RootFS/ArchLinux', 'old-fex')
    put(storage / '.local/share/fex-emu/RootFS/OtherRoot/preserve', 'unrelated FEX root')
    put(storage / '.local/share/fex-emu/RootFS/ArchLinux.sqsh', 'existing image sentinel, not an archive')
    put(storage / '.config/fex-emu/Config.json', (packet / 'packaged/Config.json').read_bytes())
    put(storage / '.config/fex-emu/AppConfig/extra.json', '{"synthetic_extra":"keep"}')


# This module is imported only inside a later allocated disposable VM fixture.
# 55-member layout is accepted evidence; these payload bytes are self-created.
def bootstrap_elf(executable=False, label=b"synthetic-only"):
    import struct
    raw = bytearray(512)
    ident = b"\x7fELF\x02\x01\x01" + b"\0" * 9
    struct.pack_into("<16sHHIQQQIHHHHHH", raw, 0, ident, 3, 183, 1,
                     0x10100 if executable else 0, 64, 0, 0, 64, 56, 2, 0, 0, 0)
    struct.pack_into("<IIQQQQQQ", raw, 64, 1, 5, 0, 0x10000, 0x10000, 512, 512, 0x1000)
    struct.pack_into("<IIQQQQQQ", raw, 120, 2, 4, 320, 0x10140, 0x10140, 16, 16, 8)
    raw[256:260] = b"\xc0\x03\x5f\xd6"  # AArch64 RET; never executed.
    raw[384:384 + len(label)] = label
    return bytes(raw)


CASES = (
    "fresh-client-real-root", "fresh-profile-dot", "fresh-profile-dot-absent", "valid-existing-alias",
    "existing-profile-dot",
    "self-updated-client", "partial-before-profile", "marker-missing-core",
    "metadata-conflict-after-profile", "crc-failure-retry", "download-failure-retry",
    "metadata-failure-retry", "interrupt-prepared-retry", "interrupt-published-retry",
    "committed-self-update-retry", "unknown-stage-before-profile",
    "transport-timeout", "validation-failure-retry", "publication-failure-retry",
    "fresh-profile-parent-alias", "existing-profile-parent-alias",
    "detached-transfer-child", "proc-census-error",
)
RETRIES = {
    "crc-failure-retry", "download-failure-retry", "metadata-failure-retry",
    "interrupt-prepared-retry", "interrupt-published-retry", "committed-self-update-retry",
    "validation-failure-retry", "publication-failure-retry",
}
RETRY_REFUSALS = {"proc-census-error"}
EARLY = {"partial-before-profile", "marker-missing-core", "unknown-stage-before-profile"}
EXISTING = {"valid-existing-alias", "self-updated-client", "existing-profile-dot", "existing-profile-parent-alias"}


def case_root(case):
    assert case in CASES
    return ALIAS_TARGET if case == "valid-existing-alias" else STEAM


def support_root(case):
    if case in ("fresh-profile-parent-alias", "existing-profile-parent-alias"):
        return Path("/storage/elsewhere/support")
    return Path("/storage/custom-profile/support") if case in ("fresh-profile-dot", "fresh-profile-dot-absent", "existing-profile-dot") else Path("/storage/.steam")


def layout():
    return json.loads((Path(__file__).resolve().parent / "layout.json").read_text())["members"]


def client_files():
    result = {}
    for row in layout():
        name = row["canonical_name"]
        if row["kind"] == "regular":
            leaf = Path(name).name
            if leaf in ("steam", "steamclient.so", "libtier0_s.so", "libvstdlib_s.so"):
                result[name] = bootstrap_elf(leaf == "steam", leaf.encode())
            elif leaf == "steamwebhelper.sh":
                result[name] = b"#!/bin/sh\n# self-created fixture only; never executed\nexit 99\n"
            else:
                result[name] = ("self-created layout sentinel: " + name + "\n").encode()
    return result


def client_archive(path, corrupt=False, invalid_core=False):
    import struct
    files = client_files()
    if invalid_core:
        files["steamrtarm64/steamclient.so"] = b"BAD!" + files["steamrtarm64/steamclient.so"][4:]
    records = []
    with zipfile.ZipFile(path, "w") as bundle:
        for row in layout():
            item = zipfile.ZipInfo(row["raw_name"], date_time=(1980, 1, 1, 0, 0, 0))
            item.create_version = item.extract_version = 20
            item.create_system = row["version_made_by"] >> 8
            item.external_attr = row["external_attributes"]
            item.compress_type = row["method"]
            data = (files[row["canonical_name"]] if row["kind"] == "regular" else
                    row["relative_target"].encode() if row["kind"] == "symlink" else b"")
            bundle.writestr(item, data)
            records.append({"raw_name": row["raw_name"], "canonical_name": row["canonical_name"],
                            "kind": row["kind"], "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                            **({"relative_target": row["relative_target"]} if row["kind"] == "symlink" else {})})
    raw = bytearray(path.read_bytes())
    good_sha = hashlib.sha256(raw).hexdigest()
    corruption = None
    if corrupt:
        selected = "steamrtarm64/chromehtml.so"  # Builddate precedes it; core entrypoint follows.
        with zipfile.ZipFile(path) as bundle:
            info = bundle.getinfo(selected)
            local, crc = info.header_offset, info.CRC
        assert raw[local:local + 4] == b"PK\x03\x04" and struct.unpack_from("<I", raw, local + 14)[0] == crc
        end = len(raw) - 22
        assert raw[end:end + 4] == b"PK\x05\x06"
        offset = struct.unpack_from("<I", raw, end + 16)[0]
        found = None
        for _ in records:
            assert raw[offset:offset + 4] == b"PK\x01\x02"
            n, x, c = struct.unpack_from("<HHH", raw, offset + 28)
            if raw[offset + 46:offset + 46 + n].decode() == selected:
                found = offset
            offset += 46 + n + x + c
        assert found is not None and offset == end and struct.unpack_from("<I", raw, found + 16)[0] == crc
        struct.pack_into("<I", raw, local + 14, crc ^ 1)
        struct.pack_into("<I", raw, found + 16, crc ^ 1)
        corruption = {"member": selected, "old_crc": crc, "wrong_crc": crc ^ 1,
                      "local_crc_offset": local + 14, "central_crc_offset": found + 16}
        path.write_bytes(raw)
    assert 0 < len(raw) < 1024**2
    return {"sha256": hashlib.sha256(raw).hexdigest(), "size": len(raw),
            "filename": "bins_linuxarm64_linuxarm64.zip." + hashlib.sha1(raw).hexdigest(),
            "uncorrupted_sha256": good_sha, "corruption": corruption, "members": records,
            "meaning": "self-created layout/CRC/bootstrap-structure input, not a native working client"}


# Keep the independent FEX/runtime/Proton data generator from the prior full
# caller; replace only client/layout/profile seeds for this candidate.
prior_build = build


def build(output, packet, installer, case):
    assert case in CASES
    prior_case = "existing-internal-alias" if case == "valid-existing-alias" else "fresh-client-real-root"
    # Keep the earlier independent runtime/FEX/Proton seeds only.
    prior_build(output, packet, installer, prior_case)
    qa, storage, jail = output / "qa", output / "storage", output / "rootfs"
    root = storage / case_root(case).relative_to("/storage")
    for name in ("layout.json", "source.json", "python-boundary.py", "exec-guard.py", "transfer-child.py"):
        put(qa / name, (packet / name).read_bytes())
    put(qa / "case.json", json.dumps({"name": case, "physical_root": str(case_root(case)), "steam": str(STEAM)}))
    put(qa / "attempt.json", '{"attempt":1}\n')
    put(qa / "client-good.json", json.dumps(client_archive(qa / "payloads/client-good.zip"), sort_keys=True))
    if case == "crc-failure-retry":
        put(qa / "client-bad.json", json.dumps(client_archive(qa / "payloads/client-bad.zip", True), sort_keys=True))
    if case == "validation-failure-retry":
        put(qa / "client-bad.json", json.dumps(client_archive(qa / "payloads/client-bad.zip", invalid_core=True), sort_keys=True))
    # The earlier synthetic ZIP carried a fake SDK payload. This one does not:
    # retain an independently seeded existing SDK and custom contents instead.
    put(root / "linuxarm64/sdk-preserve", "existing unrelated SDK bytes")
    put(root / "custom-root-file", "keep this unknown root file")
    if case in EXISTING or case == "marker-missing-core":
        for name, data in client_files().items():
            put(root / name, data, 0o755 if Path(name).name == "steam" else 0o644)
        for row in layout():
            if row["kind"] == "symlink":
                link = root / row["canonical_name"]
                link.parent.mkdir(parents=True, exist_ok=True)
                link.symlink_to(row["relative_target"])
        put(root / "steamrtarm64/custom-player-file", "keep custom client contents")
        put(root / "package/beta", "player-selected-branch\n")
        if case == "self-updated-client":
            put(root / "steamrtarm64/steamclient.so", bootstrap_elf(False, b"new-self-updated-version"))
            put(root / "package/steam_client_linuxarm64.installed", "stale synthetic marker; not readiness\n")
        if case == "marker-missing-core":
            (root / "steamrtarm64/steamclient.so").unlink()  # Only a fixture-owned synthetic seed.
            put(root / "package/steam_client_linuxarm64.installed", "marker without complete core\n")
        for name, target in (("steam", STEAM), ("sdkarm64", STEAM / "linuxarm64")):
            support = storage / support_root(case).relative_to("/storage")
            support.mkdir(parents=True, exist_ok=True)
            (support / name).symlink_to(str(target))
    elif case == "partial-before-profile":
        put(root / "steamrtarm64/00-partial", "older incomplete extraction; retain")
        put(root / "steamrtarm64\\libs\\libcurl.so", "legacy literal-backslash sibling; retain")
    elif case == "unknown-stage-before-profile":
        put(root / ".steam-client-update/unknown", "not owned by candidate; retain")
    elif case == "metadata-conflict-after-profile":
        put(root / "package/beta", "player-selected-branch\n")
    profile = (
        "export PATH=/usr/bin:/bin\n"
        "/usr/bin/python3 -I -S -B /qa/boundary.py profile\n"
        "set_kill() { /usr/bin/python3 -I -S -B /qa/boundary.py set_kill \"$@\"; }\n"
    )
    if case in ("fresh-profile-dot", "fresh-profile-dot-absent", "existing-profile-dot"):
        profile += 'STEAM_DOT="/storage/custom-profile/support"\n'
        if case != "fresh-profile-dot-absent":
            put(storage / "custom-profile/support/preserve", "profile-selected support data")
    if case in ("fresh-profile-parent-alias", "existing-profile-parent-alias"):
        # Kernel resolution is /storage/elsewhere/support; lexical normpath would
        # wrongly choose the independent /storage/support decoy.
        (storage / "elsewhere/deep").mkdir(parents=True, exist_ok=True)
        put(storage / "elsewhere/support/preserve", "real destination data")
        put(storage / "support/decoy", "lexical destination must stay untouched")
        if case == "existing-profile-parent-alias":
            put(storage / "support/steam", "unrelated regular decoy, not the real alias")
        (storage / "link").symlink_to("/storage/elsewhere/deep")
        (storage / "profile").symlink_to("link/../support")
        profile += 'STEAM_DOT="/storage/profile"\n'
    put(jail / "etc/profile", profile)
    put(qa / "guard-should-not-run", "#!/bin/sh\nprintf escaped > /qa/guard-escaped\nexit 97\n", 0o755)
