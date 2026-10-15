# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026 ROCKNIX (https://github.com/ROCKNIX)
# #582: structure is a bootstrap check, never native readiness or account proof.
import ctypes
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import selectors
import signal
import stat
import struct
import subprocess
import sys
import time
import zlib

CLIENT = "steamrtarm64"
WORK = ".steam-client-update"
LOCK = ".steam-client-update.lock"
MAX_ZIP = 128 * 1024**2
MAX_OUTPUT = 384 * 1024**2
MAX_MEMBER = 128 * 1024**2
MAX_JOURNAL = 2 * 1024**2
RESERVE = 64 * 1024**2
CORE = ("steam", "steamclient.so", "libtier0_s.so", "libvstdlib_s.so")
NAME_MAP = {
    "steamrtarm64\\libs/": "steamrtarm64/libs/",
    "steamrtarm64\\swiftshader/": "steamrtarm64/swiftshader/",
    "steamrtarm64\\libs\\libcurl.so": "steamrtarm64/libs/libcurl.so",
    "steamrtarm64\\libs\\libnghttp2.so": "steamrtarm64/libs/libnghttp2.so",
    "steamrtarm64\\libs\\libnghttp2.so.14": "steamrtarm64/libs/libnghttp2.so.14",
}
# Filled from the accepted 55-member format, not from a moving remote filename.
EXPECTED = {'steamrtarm64/libs/': 'directory',
 'steamrtarm64/swiftshader/': 'directory',
 'steamrtarm64/builddate.txt': 'file',
 'steamrtarm64/chromehtml.so': 'file',
 'steamrtarm64/crashhandler.so': 'file',
 'steamrtarm64/filesystem_stdio.so': 'file',
 'steamrtarm64/fossilize_replay': 'file',
 'steamrtarm64/friendsui.so': 'file',
 'steamrtarm64/gameoverlayrenderer.so': 'file',
 'steamrtarm64/gameoverlayui': 'file',
 'steamrtarm64/gameoverlayui.so': 'file',
 'steamrtarm64/gldriverquery': 'file',
 'steamrtarm64/icudtl.dat': 'file',
 'steamrtarm64/libVkLayer_khronos_validation.so': 'file',
 'steamrtarm64/libVkLayer_steam_fossilize.so': 'file',
 'steamrtarm64/libaom.so.3': 'file',
 'steamrtarm64/libaudio.so': 'file',
 'steamrtarm64/libdav1d.so.6': 'file',
 'steamrtarm64/libmiles.so': 'file',
 'steamrtarm64/libminigbm.so': 'file',
 'steamrtarm64/libopenvr_api.so': 'file',
 'steamrtarm64/libpulsecommon-10.0.so': 'file',
 'steamrtarm64/libs/libcurl.so': 'link',
 'steamrtarm64/libs/libcurl.so.4.8.0': 'file',
 'steamrtarm64/libs/libnghttp2.so': 'link',
 'steamrtarm64/libs/libnghttp2.so.14': 'link',
 'steamrtarm64/libs/libnghttp2.so.14.20.1': 'file',
 'steamrtarm64/libsdkencryptedappticket.so': 'file',
 'steamrtarm64/libtier0_s.so': 'file',
 'steamrtarm64/libvideo.so': 'file',
 'steamrtarm64/libvk_swiftshader.so': 'file',
 'steamrtarm64/libvstdlib_s.so': 'file',
 'steamrtarm64/libvulkan.so': 'file',
 'steamrtarm64/libvulkan.so.1': 'file',
 'steamrtarm64/reaper': 'file',
 'steamrtarm64/steam': 'file',
 'steamrtarm64/steam_monitor': 'file',
 'steamrtarm64/steamclient.so': 'file',
 'steamrtarm64/steamerrorreporter': 'file',
 'steamrtarm64/steamoverlayvulkanlayer.so': 'file',
 'steamrtarm64/steamservice.so': 'file',
 'steamrtarm64/steamsysinfo': 'file',
 'steamrtarm64/steamui.so': 'file',
 'steamrtarm64/steamwebhelper': 'file',
 'steamrtarm64/steamwebhelper.sh': 'file',
 'steamrtarm64/streaming_client': 'file',
 'steamrtarm64/swiftshader/libEGL.so': 'file',
 'steamrtarm64/swiftshader/libEGL.so.TOC': 'file',
 'steamrtarm64/swiftshader/libGLESv2.so': 'file',
 'steamrtarm64/swiftshader/libGLESv2.so.TOC': 'file',
 'steamrtarm64/v8_context_snapshot.bin': 'file',
 'steamrtarm64/vgui2_s.so': 'file',
 'steamrtarm64/vgui_panel_zoo': 'file',
 'steamrtarm64/vk_swiftshader_icd.json': 'file',
 'steamrtarm64/vulkandriverquery': 'file'}
EXECUTABLES = {
    "steam", "steam_monitor", "steamerrorreporter", "steamwebhelper",
    "steamwebhelper.sh", "gldriverquery", "vulkandriverquery",
    "steamsysinfo", "fossilize_replay", "gameoverlayui",
}
LIBC = ctypes.CDLL(None, use_errno=True)


def need(ok, text):
    if not ok:
        raise RuntimeError(text)


def identity(path):
    try:
        s = path.lstat()
    except FileNotFoundError:
        return None
    return [s.st_dev, s.st_ino, stat.S_IFMT(s.st_mode)]


def directory(path):
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts[1:]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


def open_file(path, flags=os.O_RDONLY, mode=0o600):
    parent = directory(path.parent)
    try:
        return os.open(path.name, flags | os.O_NOFOLLOW | os.O_NONBLOCK, mode, dir_fd=parent)
    finally:
        os.close(parent)


def read_file(path, maximum):
    fd = open_file(path)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_size <= maximum, "Unexpected or oversized file: " + str(path))
        with os.fdopen(fd, "rb", closefd=False) as stream:
            data = stream.read(maximum + 1)
        after = os.fstat(fd)
        need(len(data) <= maximum and stamp(before) == stamp(after), "File changed during inspection.")
        return data
    finally:
        os.close(fd)


def stamp(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def fingerprint(path):
    fd = open_file(path)
    try:
        s = os.fstat(fd)
        need(stat.S_ISREG(s.st_mode), "Expected a regular file: " + str(path))
        return stamp(s)
    finally:
        os.close(fd)


def elf(path, executable=False):
    # Bounded header/program-table reads. No loader, execution, ldd, or full-file
    # receipt comparison: legitimate self-updates may change every file digest.
    fd = open_file(path)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_size >= 64, "A core Steam file is missing or incomplete.")
        header = os.pread(fd, 64, 0)
        need(len(header) == 64 and header[:7] == b"\x7fELF\x02\x01\x01", "A core Steam file is not an ARM64 ELF.")
        _, kind, machine, version, entry, phoff, _, _, ehsize, phsize, count, _, _, _ = struct.unpack("<16sHHIQQQIHHHHHH", header)
        need(machine == 183 and version == 1 and kind in (2, 3) and (executable or kind == 3), "A core Steam file has an unsupported architecture or type.")
        need(ehsize == 64 and phsize == 56 and 0 < count <= 128 and phoff >= 64
             and phoff + count * 56 <= before.st_size, "A core Steam program table is incomplete.")
        raw = os.pread(fd, count * 56, phoff)
        need(len(raw) == count * 56, "A core Steam program table could not be read.")
        loads = []
        for i in range(count):
            typ, flags, offset, address, _, filesz, memsz, align = struct.unpack_from("<IIQQQQQQ", raw, i * 56)
            need(offset <= before.st_size and filesz <= before.st_size - offset, "A core Steam segment exceeds its file.")
            if typ == 1:
                need(filesz <= memsz and (align in (0, 1) or align & (align - 1) == 0)
                     and (align in (0, 1) or offset % align == address % align), "A core Steam load segment is invalid.")
                loads.append((flags, address, memsz))
        need(loads, "A core Steam file has no load segment.")
        if executable:
            need(before.st_mode & 0o111 and entry > 0
                 and any(flags & 1 and address <= entry < address + size for flags, address, size in loads),
                 "The Steam bootstrap entrypoint is not executable.")
        need(stamp(before) == stamp(os.fstat(fd)), "A core Steam file changed during inspection.")
        return stamp(before)
    finally:
        os.close(fd)


def bootstrap(root):
    path = root / CLIENT
    ident = identity(path)
    need(ident is not None and ident[2] == stat.S_IFDIR, "The existing Steam client folder is ambiguous.")
    fd = directory(path)
    os.close(fd)
    result = {"directory": ident, "core": {}}
    for name in CORE:
        result["core"][name] = elf(path / name, name == "steam")
    return result


def mounts_below(path):
    raw = read_file(Path("/proc") / str(os.getpid()) / "mountinfo", 1024**2)
    # proc regular files have size 0; read_file bounds bytes rather than trusting it.
    for line in raw.decode().splitlines():
        point = Path(re.sub(r"\\([0-7]{3})", lambda m: chr(int(m[1], 8)), line.split()[4]))
        need(point != path and path not in point.parents, "A client transaction path has a mounted subtree.")


def mount_rows():
    raw = read_file(Path("/proc") / str(os.getpid()) / "mountinfo", 1024**2)
    result = {}
    for line in raw.decode().splitlines():
        fields = line.split()
        separator = fields.index("-")
        need(separator >= 6 and len(fields) == separator + 4, "Storage mounts could not be inspected.")
        point = re.sub(r"\\([0-7]{3})", lambda m: chr(int(m[1], 8)), fields[4])
        result.setdefault(point, []).append(fields)
    return result


def available(path):
    rows = mount_rows()
    required = [Path("/storage")]
    for p in (Path("/storage/games-external"), Path("/storage/roms")):
        if path == p or p in path.parents:
            required.append(p)
    media = Path("/var/media")
    if media in path.parents:
        required.append(media / path.relative_to(media).parts[0])
    covers = [Path(p) for p in rows if path == Path(p) or Path(p) in path.parents]
    need(covers, "The Steam support storage is unavailable.")
    required.append(max(covers, key=lambda p: len(p.parts)))
    result = {}
    for p in set(required):
        found = rows.get(str(p), [])
        need(p != Path("/") and len(found) == 1 and "rw" in found[0][5].split(",")
             and "rw" in found[0][-1].split(","), "The Steam support storage is unavailable or read-only.")
        result[str(p)] = found[0]
    return result


def bindings(plan, root, require_root=False):
    current_mounts = mount_rows()
    need(all(current_mounts.get(point) == [fields] for point, fields in plan["mounts"].items()),
         "The Steam storage mount changed.")
    for key in ("root", "target"):
        for row in plan.get(key, {}).get("entries", []):
            path = Path(row[0])
            s = path.lstat()
            now = [str(path), s.st_dev, s.st_ino, s.st_mode]
            if stat.S_ISLNK(s.st_mode):
                now.append(os.readlink(path))
            need(now == row, "The Steam storage path changed.")
    if require_root:
        need(Path(plan["steam"]).resolve(strict=True) == root, "The Steam storage destination changed.")
        fd = directory(root)
        os.close(fd)


def consumers(root):
    # A visible installer lock is not a lock on Steam's independent updater.
    # Refuse an observed client; do not kill it or claim this scan eliminates races.
    for p in Path("/proc").iterdir():
        if not p.name.isdecimal() or int(p.name) == os.getpid():
            continue
        try:
            exe = os.readlink(p / "exe").removesuffix(" (deleted)")
            fd = os.open(p / "cmdline", os.O_RDONLY | os.O_NOFOLLOW)
            try:
                cmd = os.read(fd, 4096).split(b"\0", 1)[0].decode(errors="replace")
            finally:
                os.close(fd)
        except (FileNotFoundError, ProcessLookupError):
            continue
        except PermissionError as error:
            raise RuntimeError("Steam processes could not be checked safely.") from error
        paths = (root / CLIENT, Path(plan_global["steam"]) / CLIENT)
        need(not any(exe == str(x) or exe.startswith(str(x) + "/") or cmd.startswith(str(x) + "/") for x in paths),
             "Close Steam before installing it again.")


def journal_schema(rows, root):
    header = rows[0]
    need(header.get("op") == "header" and header.get("policy") == "arm64-bootstrap-55-v2",
         "Unsupported client ownership policy was kept.")
    work = root / WORK
    need(stat.S_IMODE(work.lstat().st_mode) == 0o700
         and work.lstat().st_uid == os.geteuid()
         and (work / "owner.jsonl").lstat().st_nlink == 1, "Client staging ownership is ambiguous.")
    meta = header["metadata"]
    committed = any(row["op"] == "committed" for row in rows)
    physical = Path(meta["dot"]["path"])
    if not committed:
        dot = probe_directory(header["dot"])
        need(dot["path"] == str(physical), "The previous support destination changed.")
        check_probe(meta["dot"])
        need(available(physical) == meta["mounts"], "The previous support storage changed.")
    need(physical != root and physical not in root.parents and root not in physical.parents
         and physical not in (Path("/storage"), Path("/var/media"), Path("/"))
         and (physical.is_relative_to("/storage") or physical.is_relative_to("/var/media")),
         "Unsupported client metadata ownership.")
    specifications = [
        (str(root / "package"), "directory", None),
        (str(root / "package/beta"), "file", "7075626c6963626574610a"),
        (str(physical), "directory", None),
        (str(physical / "steam"), "link", plan_global["steam"]),
        (str(physical / "sdkarm64"), "link", str(Path(plan_global["steam"]) / "linuxarm64")),
    ]
    need([(n["path"], n["kind"], n["value"]) for n in meta["nodes"]] == specifications,
         "Unexpected client metadata plan was kept.")
    stage_allowed = {"archive": "file", "manifest": "file", "payload": "directory"}
    for name, kind in EXPECTED.items():
        stage_allowed["payload/" + name.rstrip("/")] = kind
        for p in Path(name.rstrip("/")).parents:
            if str(p) != ".":
                stage_allowed["payload/" + str(p)] = "directory"
    external_allowed = {name: (kind, value) for name, kind, value in specifications}
    for node in meta["nodes"]:
        path = Path(node["path"]).parent
        # Extra parents may be created only along the saved absent-dot path,
        # below a pre-existing, identity-bound ancestor.
        known_dirs = {row[0] for row in meta["dot"]["entries"]}
        while path != Path("/") and str(path) not in known_dirs and path != root:
            if physical == path or path in physical.parents:
                external_allowed[str(path)] = ("directory", None)
            path = path.parent
    seen_stage, seen_external = set(), set()
    active_transfer = None
    transfer_count = 0
    for row in rows[1:]:
        op = row["op"]
        if op == "transfer-start":
            transfer_count += 1
            need(active_transfer is None and transfer_count <= 2
                 and row.get("serial") == transfer_count, "Ambiguous transfer ownership record.")
            active_transfer = transfer_count
        elif op == "transfer-stopped":
            need(active_transfer is not None and row.get("serial") == active_transfer,
                 "Unmatched transfer quiescence record.")
            active_transfer = None
        elif op == "stage":
            name = row["path"]
            need(name in stage_allowed and name not in seen_stage and row["kind"] == stage_allowed[name],
                 "Unrecognized stage ownership record.")
            seen_stage.add(name)
        elif op == "external":
            name = row["path"]
            need(name in external_allowed and name not in seen_external
                 and (row["kind"], row["value"]) == external_allowed[name], "Unrecognized metadata ownership record.")
            seen_external.add(name)
        elif op == "intent":
            need(all(n["path"] in external_allowed and (n["kind"], n["value"]) == external_allowed[n["path"]]
                     for n in row["nodes"]), "Unrecognized metadata creation intent.")
        elif op == "prepared":
            need(isinstance(row["tree"], dict) and len(row["tree"]) <= 256
                 and all(not Path(p).is_absolute() and ".." not in Path(p).parts for p in row["tree"]),
                 "Unrecognized prepared client inventory.")
        else:
            need(op in ("publishing", "committed", "failure"), "Unexpected client phase.")
        if op in ("stage", "external"):
            ident = row["id"]
            kind = {"file": stat.S_IFREG, "directory": stat.S_IFDIR, "link": stat.S_IFLNK}[row["kind"]]
            need(isinstance(ident, list) and len(ident) == 3
                 and all(type(v) is int for v in ident) and ident[2] == kind,
                 "Malformed client node identity.")


def load_journal(work, root):
    need(identity(work) is not None and identity(work)[2] == stat.S_IFDIR, "Unknown client staging state was kept.")
    mounts_below(work)
    raw = read_file(work / "owner.jsonl", MAX_JOURNAL)
    need(raw.endswith(b"\n"), "An interrupted client journal was kept for review.")
    lines = raw.splitlines(keepends=True)
    need(lines and lines[0].endswith(b"\n"), "Incomplete client ownership record was kept.")
    rows = [json.loads(line) for line in lines if line.endswith(b"\n")]
    h = rows[0]
    need(h.get("format") == 1 and h.get("root") == str(root)
         and h.get("root_id") == identity(root) and h.get("work_id") == identity(work)
         and h.get("journal_id") == identity(work / "owner.jsonl"), "Client ownership changed; existing state was kept.")
    need(len(rows) <= 512 and all(isinstance(row, dict) for row in rows), "Unsupported client ownership record.")
    allowed = {"header", "stage", "external", "intent", "prepared", "publishing", "committed", "failure", "transfer-start", "transfer-stopped"}
    need(all(row.get("op") in allowed for row in rows), "Unknown client transaction phase was kept.")
    journal_schema(rows, root)
    tx = Transaction(root, h["dot"], h["metadata"], rows)
    tx.check_owned_state()
    if any(row["op"] == "committed" for row in rows):
        bootstrap(root)  # A committed client's updater may legitimately change bytes.
    elif tx.published():
        need(tx.tree(root / CLIENT) == tx.prepared()["tree"], "An uncommitted published client changed; it was kept.")
    return rows


def inspect_tree(plan, root, check_lock=True):
    bindings(plan, root)
    consumers(root)
    if check_lock and identity(root / LOCK) is not None:
        fd = open_file(root / LOCK)
        try:
            need(stat.S_ISREG(os.fstat(fd).st_mode), "The client lock is ambiguous.")
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)
    work = root / WORK
    if identity(work) is not None:
        rows = load_journal(work, root)
        # Recovery runs later under the lock. This read-only branch does not
        # bless an existing directory as installed, or normalize old contents.
        return {"kind": "recovery", "root": str(root), "work_id": identity(work),
                "journal_id": identity(work / "owner.jsonl"), "dot": rows[0]["dot"],
                "committed": any(row["op"] == "committed" for row in rows)}
    if identity(root / CLIENT) is not None:
        return {"kind": "existing", "root": str(root), "bootstrap": bootstrap(root)}
    for name in ("linuxarm64.zip", "steamrtarm64\\libs", "steamrtarm64\\swiftshader",
                 "steamrtarm64\\libs\\libcurl.so", "steamrtarm64\\libs\\libnghttp2.so", "steamrtarm64\\libs\\libnghttp2.so.14"):
        need(identity(root / name) is None, "An earlier Steam download is incomplete. Its files were kept.")
    return {"kind": "fresh", "root": str(root)}


def probe_directory(value):
    path = Path(value)
    need(path.is_absolute() and str(path) == os.path.normpath(value) and not value.startswith("//")
         and not any(ord(c) < 32 for c in value), "The Steam support folder path is ambiguous.")
    entries = []
    current = Path("/")
    pending = list(path.parts[1:])
    links = 0
    while pending:
        part = pending.pop(0)
        if part in ("", "."):
            continue
        if part == "..":
            current = current.parent
            continue
        candidate = current / part
        ident = identity(candidate)
        if ident is None:
            need(".." not in pending, "A missing support folder precedes a parent traversal.")
            return {"input": value, "path": str(candidate.joinpath(*pending)), "entries": entries, "exists": False}
        s = candidate.lstat()
        row = [str(candidate), *ident]
        if stat.S_ISLNK(s.st_mode):
            links += 1
            need(links <= 40, "The Steam support folder has too many links.")
            target = os.readlink(candidate)
            need(target and not any(ord(c) < 32 for c in target), "The Steam support folder link is ambiguous.")
            row.append(target)
            entries.append(row)
            # Resolve each target component before applying any following '..'.
            # Lexical normpath would erase a preceding directory symlink.
            pending = target.split("/") + pending
            if target.startswith("/"):
                current = Path("/")
        else:
            need(stat.S_ISDIR(s.st_mode), "A file is blocking the Steam support folder.")
            entries.append(row)
            current = candidate
    return {"input": value, "path": str(current), "entries": entries, "exists": True}


def check_probe(probe):
    for row in probe["entries"]:
        path = Path(row[0])
        now = [str(path), *(identity(path) or [])]
        if path.is_symlink():
            now.append(os.readlink(path))
        need(now == row, "The Steam support folder changed.")
    need(probe_directory(probe["input"])["path"] == probe["path"],
         "The logical Steam support destination changed.")


def describe(path):
    ident = identity(path)
    if ident is None:
        return None
    if ident[2] == stat.S_IFLNK:
        return {"id": ident, "target": os.readlink(path)}
    if ident[2] == stat.S_IFREG:
        return {"id": ident, "bytes": read_file(path, 4096).hex(), "stamp": fingerprint(path)}
    need(ident[2] == stat.S_IFDIR, "Unsupported Steam metadata entry.")
    return {"id": ident}


def metadata(root, dot_value, tree):
    dot = probe_directory(dot_value)
    physical = Path(dot["path"])
    need(physical not in (Path("/"), Path("/storage"), Path("/var/media")) and physical != root and root not in physical.parents
         and physical not in root.parents, "The Steam support folder overlaps client storage.")
    # Preserve profile-selected paths, but require them on available /storage or
    # /var/media storage. Root-path/mount admission remains the shared root helper.
    need(physical.is_relative_to("/storage") or physical.is_relative_to("/var/media"), "The Steam support folder is outside supported storage.")
    if tree["kind"] == "existing":
        need(dot["exists"], "The existing client support folder is missing. Existing files were kept.")
    nodes = [
        (root / "package", "directory", None),
        (root / "package/beta", "file", "7075626c6963626574610a"),
        (physical, "directory", None),
        (physical / "steam", "link", plan_global["steam"]),
        (physical / "sdkarm64", "link", str(Path(plan_global["steam"]) / "linuxarm64")),
    ]
    result = {"dot": dot, "mounts": available(physical), "nodes": []}
    for path, kind, value in nodes:
        before = describe(path)
        if before is not None:
            if kind == "directory":
                need(before["id"][2] == stat.S_IFDIR, "A Steam metadata directory is blocked.")
            elif tree["kind"] == "fresh":
                equal = before.get("bytes") == value if kind == "file" else (
                    "target" in before and os.path.realpath(path) == os.path.realpath(value))
                need(equal, "Existing Steam support settings were kept. Fresh setup cannot replace them.")
            elif kind == "file":
                need(before["id"][2] == stat.S_IFREG, "The existing Steam channel entry is ambiguous.")
            else:
                need(before["id"][2] == stat.S_IFLNK, "An existing Steam support alias is ambiguous.")
            # Existing client channels and aliases belong to Steam/the player:
            # inspect their types but neither replace them nor assert readiness.
        result["nodes"].append({"path": str(path), "kind": kind, "value": value, "before": before})
    return result


def same_metadata(saved, root, dot, tree):
    current = metadata(root, dot, tree)
    need(current == saved, "Steam support settings changed during installation.")
    check_probe(saved["dot"])


def digest_file(path, maximum):
    fd = open_file(path)
    try:
        s = os.fstat(fd)
        need(stat.S_ISREG(s.st_mode) and s.st_size <= maximum, "Unexpected client file size or type.")
        h = hashlib.sha256()
        with os.fdopen(fd, "rb", closefd=False) as stream:
            while chunk := stream.read(65536):
                h.update(chunk)
        need(stamp(s) == stamp(os.fstat(fd)), "A client file changed during validation.")
        return h.hexdigest()
    finally:
        os.close(fd)


def manifest(raw):
    need(len(raw) <= 2 * 1024**2, "Steam manifest exceeded its limit.")
    text = raw.decode("ascii")
    tokens, end = [], 0
    for match in re.finditer(r'"(?:[^"\\]|\\.)*"|[{}]', text):
        need(not text[end:match.start()].strip(), "Unrecognized Steam manifest syntax.")
        tokens.append(match.group())
        end = match.end()
    need(not text[end:].strip() and len(tokens) < 5000, "Steam manifest exceeded its syntax limits.")
    pos = 0
    def obj(depth=0):
        nonlocal pos
        need(depth < 8, "Steam manifest nesting exceeded its limit.")
        result = {}
        while pos < len(tokens) and tokens[pos] != "}":
            key = json.loads(tokens[pos])
            pos += 1
            need(isinstance(key, str) and key not in result and pos < len(tokens), "Ambiguous Steam manifest key.")
            token = tokens[pos]
            pos += 1
            if token == "{":
                result[key] = obj(depth + 1)
                need(pos < len(tokens) and tokens[pos] == "}", "Incomplete Steam manifest.")
                pos += 1
            else:
                result[key] = json.loads(token)
        return result
    tree = obj()
    need(pos == len(tokens), "Trailing Steam manifest data.")
    selected = tree["linuxarm64"]["bins_linuxarm64_linuxarm64"]
    name, checksum, size = selected["file"], selected["sha2"], selected["size"]
    need(isinstance(name, str) and re.fullmatch(r"bins_linuxarm64_linuxarm64\.zip\.[0-9a-f]{40}", name)
         and isinstance(checksum, str) and re.fullmatch(r"[0-9a-f]{64}", checksum)
         and isinstance(size, str) and re.fullmatch(r"[0-9]{1,9}", size), "Unsupported Steam package selection.")
    size = int(size)
    need(22 <= size <= MAX_ZIP, "Steam client archive exceeds the supported size.")
    return name, checksum, size


def process_identity(pid):
    path = Path("/proc") / str(pid)
    try:
        raw = read_file(path / "stat", 16384).decode()
    except (FileNotFoundError, ProcessLookupError):
        # A disappeared PID is a normal race. A present PID with unreadable stat
        # is a visibility failure, never evidence of an empty process census.
        need(identity(path) is None, "A live process identity could not be read.")
        return None
    prefix, separator, suffix = raw.rpartition(")")
    fields = suffix.split()
    need(separator and prefix.startswith(str(pid) + " (") and len(fields) >= 20,
         "Malformed process identity; client state was kept.")
    ppid, start = int(fields[1]), int(fields[19])
    need(ppid >= 0 and start >= 0, "Invalid process owner or start time.")
    return {"pid": pid, "ppid": ppid, "start_ticks": start}


def direct_children(deadline):
    # /proc/PID/task/PID/children is optional on the target kernel. The numeric
    # stat census is the already-used PPID/start-time contract instead.
    owner = os.getpid()
    result, seen_owner, count = [], False, 0
    for path in Path("/proc").iterdir():
        if not path.name.isdecimal():
            continue
        count += 1
        need(count <= 65536 and time.monotonic() < deadline, "Process census exceeded its bound.")
        row = process_identity(int(path.name))
        if row is not None:
            seen_owner |= row["pid"] == owner
            if row["ppid"] == owner:
                result.append(row)
    need(seen_owner, "Process census does not show this supervisor.")
    return result


def terminate_group(proc):
    # Always retire the group, including successful drivers' leftover children.
    # The helper is a subreaper: orphaned setsid descendants become its children.
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    proc.wait(timeout=5)
    deadline = time.monotonic() + 5
    while True:
        try:
            pid, _ = os.waitpid(-1, os.WNOHANG)
        except ChildProcessError:
            return  # Kernel ECHILD after the leader was reaped is quiescence.
        need(time.monotonic() < deadline, "A client transfer child did not retire.")
        if pid:
            continue
        for row in direct_children(deadline):
            need(time.monotonic() < deadline, "Transfer child cleanup exceeded its bound.")
            try:
                pfd = os.pidfd_open(row["pid"], 0)
            except ProcessLookupError:
                continue
            try:
                current = process_identity(row["pid"])
                if current is None:
                    continue
                need(current == row and current["ppid"] == os.getpid(),
                     "A transfer child identity changed; client state was kept.")
                try:
                    signal.pidfd_send_signal(pfd, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            finally:
                os.close(pfd)
        time.sleep(0.01)


def transfer(url, fd, limit, seconds, quiescent):
    argv = ["curl", "--disable", "--fail", "--silent", "--show-error", "--location",
            "--proto", "=https", "--proto-redir", "=https", "--max-redirs", "5",
            "--connect-timeout", "10", "--max-time", str(seconds),
            "--max-filesize", str(limit), "--output", "-", url]
    parent = os.getpid()
    def child_limits():
        resource.setrlimit(resource.RLIMIT_FSIZE, (limit, limit))
        if LIBC.prctl(1, signal.SIGKILL, 0, 0, 0) or os.getppid() != parent:
            os._exit(125)
    proc = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=fd, stderr=subprocess.PIPE,
                            start_new_session=True, preexec_fn=child_limits)
    errors = bytearray()
    deadline = time.monotonic() + seconds + 2
    selector = None
    try:
        selector = selectors.DefaultSelector()
        selector.register(proc.stderr, selectors.EVENT_READ)
        while selector.get_map():
            need(time.monotonic() < deadline, "Steam client transfer timed out.")
            for key, _ in selector.select(0.1):
                block = os.read(key.fd, 8192)
                if not block:
                    selector.unregister(key.fileobj)
                else:
                    errors.extend(block)
                    need(len(errors) <= 65536, "Steam client transfer log exceeded its limit.")
        code = proc.wait(timeout=max(0.01, deadline - time.monotonic()))
        need(code == 0, "Steam client transfer failed (exit " + str(code) + ").")
        os.fsync(fd)
    finally:
        try:
            if selector is not None:
                selector.close()
            proc.stderr.close()
        finally:
            terminate_group(proc)
            # An exception, visibility gap or deadline before ECHILD must leave
            # a durable unmatched transfer-start. Never authorize stage cleanup.
            quiescent()


def rename_new(source, target):
    a, b = directory(source.parent), directory(target.parent)
    try:
        need(LIBC.renameat2(a, os.fsencode(source.name), b, os.fsencode(target.name), 1) == 0,
             "The new Steam client could not be published without replacing an existing path.")
        os.fsync(a)
        os.fsync(b)
    finally:
        os.close(a)
        os.close(b)


class Transaction:
    def __init__(self, root, dot, meta, rows=None):
        self.root, self.work, self.dot, self.meta = root, root / WORK, dot, meta
        self.rows = rows or []
        self.journal = None

    def append(self, row):
        self.rows.append(row)  # Active cleanup knows identity even if journaling fails.
        raw = (json.dumps(row, sort_keys=True) + "\n").encode()
        need(os.fstat(self.journal).st_size + len(raw) <= MAX_JOURNAL, "Client journal exceeded its limit.")
        need(os.write(self.journal, raw) == len(raw), "Short client journal write.")
        os.fsync(self.journal)

    def begin(self):
        self.work.mkdir(mode=0o700)
        self.journal = open_file(self.work / "owner.jsonl", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_APPEND)
        self.append({"op": "header", "format": 1, "policy": "arm64-bootstrap-55-v2", "root": str(self.root), "root_id": identity(self.root),
                     "work_id": identity(self.work), "journal_id": identity(self.work / "owner.jsonl"),
                     "dot": self.dot, "metadata": self.meta})
        fd = directory(self.root)
        os.fsync(fd)
        os.close(fd)

    def add(self, relative, kind, data=None):
        path = self.work / relative
        need(not Path(relative).is_absolute() and ".." not in Path(relative).parts, "Invalid owned stage name.")
        if kind == "directory":
            parent = directory(path.parent)
            try:
                os.mkdir(path.name, 0o700, dir_fd=parent)
            finally:
                os.close(parent)
            self.append({"op": "stage", "path": relative, "id": identity(path), "kind": kind})
            return None
        if kind == "link":
            parent = directory(path.parent)
            try:
                os.symlink(data, path.name, dir_fd=parent)
            finally:
                os.close(parent)
            self.append({"op": "stage", "path": relative, "id": identity(path), "kind": kind, "target": data})
            return None
        fd = open_file(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        try:
            self.append({"op": "stage", "path": relative, "id": identity(path), "kind": "file"})
        except BaseException:
            os.close(fd)
            raise
        return fd

    def put(self, relative, data):
        fd = self.add(relative, "file")
        try:
            need(os.write(fd, data) == len(data), "Short staging write.")
            os.fsync(fd)
        finally:
            os.close(fd)

    def download(self, url, fd, limit, seconds):
        serial = 1 + sum(row["op"] == "transfer-start" for row in self.rows)
        self.append({"op": "transfer-start", "serial": serial})
        transfer(url, fd, limit, seconds,
                 lambda: self.append({"op": "transfer-stopped", "serial": serial}))

    def fetch(self):
        fd = self.add("manifest", "file")
        try:
            self.download("https://client-update.fastly.steamstatic.com/steam_client_publicbeta_linuxarm64", fd, 2 * 1024**2, 30)
        finally:
            os.close(fd)
        name, checksum, size = manifest(read_file(self.work / "manifest", 2 * 1024**2))
        need(os.statvfs(self.root).f_bavail * os.statvfs(self.root).f_frsize >= size + MAX_OUTPUT + RESERVE,
             "There is not enough free space to prepare the Steam client.")
        fd = self.add("archive", "file")
        try:
            self.download("https://client-update.steamstatic.com/" + name, fd, size, 180)
        finally:
            os.close(fd)
        need((self.work / "archive").stat().st_size == size and digest_file(self.work / "archive", MAX_ZIP) == checksum,
             "The Steam client download did not match its manifest.")
        return size, checksum

    def extract(self, size):
        archive = self.work / "archive"
        fd = open_file(archive)
        rows = []
        try:
            def read(offset, length):
                need(0 <= offset <= size and 0 <= length <= size - offset, "ZIP record exceeds the archive.")
                raw = os.pread(fd, length, offset)
                need(len(raw) == length, "Incomplete ZIP record.")
                return raw
            sig, disk, cd_disk, count_disk, count, cd_size, cd_start, comment = struct.unpack("<4s4H2IH", read(size - 22, 22))
            need(sig == b"PK\x05\x06" and disk == cd_disk == comment == 0 and count_disk == count
                 and count == len(EXPECTED) <= 128 and cd_start + cd_size == size - 22 and cd_size <= 65536,
                 "Unsupported Steam ZIP directory.")
            central = read(cd_start, cd_size)
            pos, next_local, expanded, seen = 0, None, 0, set()
            for _ in range(count):
                need(pos + 46 <= len(central), "Incomplete ZIP directory.")
                fields = struct.unpack_from("<4s6H3I5H2I", central, pos)
                sig, made, required, flags, method, mtime, mdate, crc, packed, unpacked, nlen, extra, note, disk, _, attr, local = fields
                need(sig == b"PK\x01\x02" and flags == extra == note == disk == 0 and required == 20
                     and method in (0, 8) and pos + 46 + nlen <= len(central), "Unsupported Steam ZIP member.")
                name_bytes = central[pos + 46:pos + 46 + nlen]
                name = name_bytes.decode("ascii")
                canonical = NAME_MAP.get(name, name)
                kind = EXPECTED.get(canonical)
                need(kind is not None and canonical not in seen and "\\" not in canonical
                     and all(part not in ("", ".", "..") for part in canonical.rstrip("/").split("/")),
                     "Unexpected or duplicate Steam ZIP path.")
                seen.add(canonical)
                if kind == "directory":
                    need(method == 0 and unpacked == packed == crc == 0 and made == 20 and attr == 0x40000000,
                         "Unexpected Steam directory attributes.")
                elif kind == "link":
                    need(made == 788 and stat.S_IFMT(attr >> 16) == stat.S_IFLNK and method == 0
                         and 0 < unpacked == packed <= 4096, "Unexpected stored Steam link.")
                else:
                    need(made == 20 and attr == 2176188416 and method == 8, "Unsupported Steam file attributes.")
                need(unpacked <= MAX_MEMBER, "Steam ZIP member exceeds its output limit.")
                expanded += unpacked
                need(expanded <= MAX_OUTPUT, "Steam ZIP exceeds its total output limit.")
                if next_local is None:
                    need(local in (0, 20), "Unsupported ZIP prefix.")
                else:
                    need(local == next_local, "Overlapping or unlisted ZIP local data.")
                header = struct.unpack("<4s5H3I2H", read(local, 30))
                need(header == (b"PK\x03\x04", required, flags, method, mtime, mdate, crc, packed, unpacked, nlen, 0)
                     and read(local + 30, nlen) == name_bytes, "ZIP local and central records disagree.")
                offset = local + 30 + nlen
                next_local = offset + packed
                need(next_local <= cd_start, "ZIP payload overlaps its directory.")
                rows.append({"name": canonical, "kind": kind, "offset": offset, "packed": packed,
                             "bytes": unpacked, "crc": crc, "method": method})
                pos += 46 + nlen
            need(pos == len(central) and next_local == cd_start and seen == set(EXPECTED), "Incomplete Steam ZIP inventory.")
            self.add("payload", "directory")
            dirs = {str(Path(row["name"]).parent) for row in rows}
            dirs |= {row["name"].rstrip("/") for row in rows if row["kind"] == "directory"}
            dirs.discard(".")
            for name in sorted(dirs, key=lambda x: (len(Path(x).parts), x)):
                self.add("payload/" + name, "directory")
            deadline, total, links, receipt = time.monotonic() + 90, 0, [], []
            for row in rows:
                if row["kind"] == "directory":
                    continue
                target = "payload/" + row["name"]
                out = self.add(target, "file") if row["kind"] == "file" else None
                unpacker = zlib.decompressobj(-15) if row["method"] == 8 else None
                length, crc, sha, link = 0, 0, hashlib.sha256(), bytearray()
                try:
                    remaining, offset = row["packed"], row["offset"]
                    while remaining:
                        chunk = read(offset, min(65536, remaining))
                        remaining -= len(chunk)
                        offset += len(chunk)
                        while chunk:
                            need(time.monotonic() < deadline, "Steam ZIP decoding timed out.")
                            data = unpacker.decompress(chunk, 65536) if unpacker else chunk
                            chunk = unpacker.unconsumed_tail if unpacker else b""
                            length += len(data)
                            total += len(data)
                            need(length <= row["bytes"] and total <= MAX_OUTPUT, "Steam ZIP produced too much output.")
                            crc = zlib.crc32(data, crc)
                            sha.update(data)
                            if out is None:
                                link.extend(data)
                            else:
                                need(os.write(out, data) == len(data), "Short Steam client write.")
                            if unpacker:
                                need(not unpacker.unused_data, "Trailing compressed Steam data.")
                    need(length == row["bytes"] and crc == row["crc"] and (not unpacker or unpacker.eof),
                         "Steam client CRC, length, or compressed stream verification failed.")
                    if out is not None:
                        os.fchmod(out, 0o755 if Path(row["name"]).name in EXECUTABLES else 0o644)
                        os.fsync(out)
                    else:
                        value = link.decode("ascii")
                        need(value not in ("", ".", "..") and "/" not in value and "\\" not in value
                             and not any(ord(c) < 32 for c in value)
                             and EXPECTED.get(str(Path(row["name"]).parent / value)) == "file",
                             "Steam link target is outside the validated client.")
                        links.append((target, value))
                    receipt.append({"path": row["name"], "kind": row["kind"], "bytes": length, "sha256": sha.hexdigest()})
                finally:
                    if out is not None:
                        os.close(out)
            for target, value in links:
                self.add(target, "link", value)
            for name in dirs:
                os.chmod(self.work / "payload" / name, 0o755, follow_symlinks=False)
            bootstrap(self.work / "payload")
            tree = self.tree(self.work / "payload" / CLIENT)
            self.append({"op": "prepared", "client_id": identity(self.work / "payload" / CLIENT),
                         "tree": tree, "members": receipt})
        finally:
            os.close(fd)

    def tree(self, path):
        mounts_below(path)
        result = {}
        for base, dirs, files in os.walk(path, followlinks=False):
            need(len(result) <= 256, "The staged client has too many paths.")
            for name in dirs + files:
                p = Path(base) / name
                s = p.lstat()
                key = str(p.relative_to(path))
                entry = {"id": identity(p), "mode": stat.S_IMODE(s.st_mode)}
                if stat.S_ISLNK(s.st_mode):
                    entry["target"] = os.readlink(p)
                elif stat.S_ISREG(s.st_mode):
                    need(s.st_nlink == 1, "The staged client has a hard link.")
                    entry.update(bytes=s.st_size, sha256=digest_file(p, MAX_MEMBER))
                else:
                    need(stat.S_ISDIR(s.st_mode), "Unexpected staged client node.")
                result[key] = entry
        return result

    def prepare_metadata(self):
        check_probe(self.meta["dot"])
        need(available(Path(self.meta["dot"]["path"])) == self.meta["mounts"],
             "The support storage changed before metadata writes.")
        self.append({"op": "intent", "nodes": self.meta["nodes"]})
        for node in self.meta["nodes"]:
            path = Path(node["path"])
            if node["before"] is not None:
                need(describe(path) == node["before"], "Steam support settings changed.")
                continue
            # Only absent parents/nodes are created, never substituted for
            # existing aliases, channels, SDK trees or custom files.
            missing = []
            parent = path.parent
            while identity(parent) is None:
                missing.append(parent)
                parent = parent.parent
            for p in reversed(missing):
                self.external(p, "directory", None)
            self.external(path, node["kind"], node["value"])

    def external(self, path, kind, value):
        check_probe(self.meta["dot"])
        self.append({"op": "intent", "nodes": [{"path": str(path), "kind": kind, "value": value, "before": None}]})
        need(identity(path) is None, "A Steam metadata destination appeared.")
        parent = directory(path.parent)
        parent_id = identity(path.parent)
        try:
            if kind == "directory":
                os.mkdir(path.name, 0o755, dir_fd=parent)
            elif kind == "link":
                os.symlink(value, path.name, dir_fd=parent)
            else:
                fd = os.open(path.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644, dir_fd=parent)
                try:
                    data = bytes.fromhex(value)
                    need(os.write(fd, data) == len(data), "Short Steam metadata write.")
                    os.fsync(fd)
                finally:
                    os.close(fd)
            self.append({"op": "external", "path": str(path), "id": identity(path),
                         "parent_id": parent_id, "kind": kind, "value": value})
            os.fsync(parent)
        finally:
            os.close(parent)

    def prepared(self):
        rows = [row for row in self.rows if row["op"] == "prepared"]
        need(len(rows) <= 1, "Ambiguous prepared client record.")
        return rows[0] if rows else None

    def published(self):
        prepared = self.prepared()
        return prepared is not None and identity(self.root / CLIENT) == prepared["client_id"]

    def check_external(self, row):
        path = Path(row["path"])
        need(identity(path.parent) == row["parent_id"], "A client metadata parent changed; state was kept.")
        current = describe(path)
        need(current is not None and current["id"] == row["id"], "Client metadata ownership changed; state was kept.")
        if row["kind"] == "file":
            need(current.get("bytes") == row["value"], "Client metadata contents changed; state was kept.")
        elif row["kind"] == "link":
            need(current.get("target") == row["value"], "Client metadata link changed; state was kept.")

    def commit(self):
        need(self.published(), "Published client identity changed.")
        prepared = self.prepared()
        need(self.tree(self.root / CLIENT) == prepared["tree"], "The published client changed before commit.")
        for row in self.rows:
            if row["op"] == "external":
                self.check_external(row)
        for node in self.meta["nodes"]:
            if node["before"] is not None:
                need(describe(Path(node["path"])) == node["before"], "Existing Steam metadata changed before commit.")
        self.append({"op": "committed"})
        self.cleanup(keep_client=True)

    def check_owned_state(self):
        starts = [row["serial"] for row in self.rows if row["op"] == "transfer-start"]
        stops = [row["serial"] for row in self.rows if row["op"] == "transfer-stopped"]
        need(starts == stops, "Transfer quiescence is unestablished; client staging was kept for review.")
        bindings(plan_global, self.root, True)
        need(identity(self.work) == self.rows[0]["work_id"] and identity(self.work / "owner.jsonl") == self.rows[0]["journal_id"],
             "Client stage ownership changed; state was kept.")
        mounts_below(self.work)
        stage = [row for row in self.rows if row["op"] == "stage"]
        known = {row["path"]: row for row in stage}
        actual = set()
        for base, dirs, files in os.walk(self.work, followlinks=False):
            for name in dirs + files:
                p = Path(base) / name
                relative = str(p.relative_to(self.work))
                if relative == "owner.jsonl":
                    continue
                need(relative in known and identity(p) == known[relative]["id"], "Unknown or changed stage contents were kept.")
                need(p.lstat().st_dev == self.work.stat().st_dev and
                     (not p.is_file() or p.lstat().st_nlink == 1), "A client stage crosses an ownership boundary.")
                actual.add(relative)
        # Unrecorded creation after interruption is deliberately held. No
        # ownership is inferred from a familiar filename or partial journal.
        external = [row for row in self.rows if row["op"] == "external"]
        owned = {row["path"] for row in external}
        for row in self.rows:
            if row["op"] == "intent":
                for node in row["nodes"]:
                    if node["before"] is None and identity(Path(node["path"])) is not None:
                        need(node["path"] in owned, "Unrecorded client metadata was kept for review.")
        committed = any(row["op"] == "committed" for row in self.rows)
        if not committed:
            for row in external:
                if identity(Path(row["path"])) is not None or self.published():
                    self.check_external(row)
        return known, actual, external

    def cleanup(self, keep_client=False):
        known, actual, external = self.check_owned_state()
        if not keep_client:
            need(not self.published(), "A published client must be verified before recovery.")
            for row in external:
                if identity(Path(row["path"])) is not None:
                    self.check_external(row)
            for row in reversed(external):
                self.remove(Path(row["path"]), row["id"], row["kind"])
        for relative in sorted(actual, key=lambda x: (len(Path(x).parts), x), reverse=True):
            row = known[relative]
            self.remove(self.work / relative, row["id"], row["kind"])
        if self.journal is not None:
            os.close(self.journal)
            self.journal = None
        self.remove(self.work / "owner.jsonl", self.rows[0]["journal_id"], "file")
        self.remove(self.work, self.rows[0]["work_id"], "directory")

    def remove(self, path, expected, kind):
        if identity(path) is None:
            return  # An earlier interrupted cleanup already retired this owned node.
        parent = directory(path.parent)
        try:
            s = os.stat(path.name, dir_fd=parent, follow_symlinks=False)
            need([s.st_dev, s.st_ino, stat.S_IFMT(s.st_mode)] == expected, "Client cleanup identity changed.")
            if kind == "directory":
                os.rmdir(path.name, dir_fd=parent)
            else:
                os.unlink(path.name, dir_fd=parent)
            os.fsync(parent)
        finally:
            os.close(parent)


def install(root, tree, meta, dot):
    bindings(plan_global, root, True)
    consumers(root)
    lock = open_file(root / LOCK, os.O_RDWR | os.O_CREAT, 0o600)
    try:
        s = os.fstat(lock)
        need(stat.S_ISREG(s.st_mode) and s.st_nlink == 1, "The client lock is ambiguous.")
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        work = root / WORK
        if identity(work) is not None:
            rows = load_journal(work, root)
            committed = any(row["op"] == "committed" for row in rows)
            need(committed or rows[0]["dot"] == dot, "Recovery needs the same profile-selected Steam support folder.")
            tx = Transaction(root, dot, rows[0]["metadata"], rows)
            if not committed:
                check_probe(tx.meta["dot"])
            tx.journal = open_file(work / "owner.jsonl", os.O_WRONLY | os.O_APPEND)
            try:
                if committed:
                    tx.cleanup(keep_client=True)
                    print("An existing Steam client was kept; completed setup scratch was retired.")
                    return
                if tx.published():
                    tx.commit()
                    print("Steam client file setup recovered.")
                    return
                tx.cleanup()
            finally:
                if tx.journal is not None:
                    os.close(tx.journal)
            # Do not turn a recovered failure into a successful installed state.
            # This same explicit invocation can start a fresh bounded download.
            tree = inspect_tree(plan_global, root, False)
            meta = metadata(root, dot, tree)
        else:
            need(inspect_tree(plan_global, root, False) == tree, "The Steam client changed during installation.")
            same_metadata(meta, root, dot, tree)
        if tree["kind"] == "existing":
            print("Existing Steam client files were kept.")
            return
        need(tree["kind"] == "fresh" and identity(root / CLIENT) is None, "Steam client state is ambiguous.")
        need(os.statvfs(root).f_bavail * os.statvfs(root).f_frsize >= MAX_ZIP + MAX_OUTPUT + RESERVE,
             "There is not enough free space to prepare the Steam client.")
        tx = Transaction(root, dot, meta)
        try:
            tx.begin()
            size, _ = tx.fetch()
            tx.extract(size)
            bindings(plan_global, root, True)
            consumers(root)
            same_metadata(meta, root, dot, tree)
            tx.prepare_metadata()
            tx.append({"op": "publishing"})
            rename_new(work / "payload" / CLIENT, root / CLIENT)
            tx.commit()
        except BaseException:
            if tx.rows and tx.journal is not None:
                try:
                    tx.append({"op": "failure"})
                    if not tx.published():
                        tx.cleanup()
                except BaseException as cleanup_error:
                    print("Steam client recovery state was kept: " + str(cleanup_error), file=sys.stderr)
            raise
        finally:
            if tx.journal is not None:
                os.close(tx.journal)
        print("Steam client files are in place.")
    finally:
        os.close(lock)


def interrupted(signum, frame):
    raise RuntimeError("Steam client setup was interrupted (signal " + str(signum) + ").")


def main():
    global plan_global
    mode, plan_text, dot, tree_text, meta_text = sys.argv[1:]
    plan_global = json.loads(plan_text)
    root = Path(plan_global.get("target", plan_global["root"])["path"])
    for sig in (signal.SIGALRM, signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, interrupted)
    signal.alarm(360 if mode == "install" else 30)
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2, 512 * 1024**2))
    if mode == "tree":
        print(json.dumps(inspect_tree(plan_global, root), sort_keys=True))
        return
    tree = json.loads(tree_text)
    if mode == "metadata":
        need(inspect_tree(plan_global, root) == tree, "The Steam client changed while profiles loaded.")
        if tree["kind"] == "recovery" and not tree["committed"]:
            need(tree["dot"] == dot, "Recovery needs the same profile-selected Steam support folder.")
            rows = load_journal(root / WORK, root)
            print(json.dumps(rows[0]["metadata"], sort_keys=True))
        else:
            print(json.dumps(metadata(root, dot, {"kind": "existing"} if tree["kind"] == "recovery" else tree), sort_keys=True))
        return
    need(mode == "install", "Unsupported Steam client operation.")
    need(LIBC.prctl(36, 1, 0, 0, 0) == 0, "Client transfer child supervision is unavailable.")
    install(root, tree, json.loads(meta_text), dot)


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, ValueError, KeyError, TypeError, IndexError, struct.error, zlib.error, subprocess.SubprocessError) as error:
        print("Steam client setup stopped: " + str(error), file=sys.stderr)
        sys.exit(1)
