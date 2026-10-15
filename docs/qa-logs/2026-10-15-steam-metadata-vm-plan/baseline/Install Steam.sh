#!/bin/bash

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)

set -e
set -o pipefail

STEAM="${STEAM:-/storage/.local/share/Steam}"
STEAM_GAMES_ROOT="${STEAM_GAMES_ROOT:-/storage/games-internal/roms/steam}"
# --- Logging & Error Handling Helpers ---
log_info() { echo -e "[\033[1;34mINFO\033[0m] $1"; }
log_success() { echo -e "[\033[1;32mSUCCESS\033[0m] $1"; sleep 10; exit 0; }
die() { echo -e "[\033[1;31mERROR\033[0m] $1" >&2; sleep 10; exit 1; }
# ----------------------------------------

# Inspect before profiles or installer functions can write. The saved plan is
# process-local; no marker, directory, lock, or test file is created by preflight.
steam_root_layout() {
  /usr/bin/python3 -I -S -B - "$1" "${STEAM}" "${STEAM_GAMES_ROOT}" "${STEAM_ROOT_PLAN:-}" <<'PY_STEAM_ROOT'
import json
import os
from pathlib import Path
import re
import stat
import sys

STORAGE = Path("/storage")
MOUNTINFO = Path("/proc/self/mountinfo")
MEDIA = Path("/var/media")


def beneath(path, parent):
    return path == parent or parent in path.parents


def input_path(value):
    if (not value.startswith("/") or value != os.path.normpath(value)
            or value.startswith("//") or any(ord(c) < 32 for c in value)):
        raise ValueError("The Steam folder path is not an absolute, unambiguous path.")
    return Path(value)


def read_mounts():
    with MOUNTINFO.open() as stream:
        raw = stream.read(1024 * 1024 + 1)
    if not raw or len(raw) > 1024 * 1024:
        raise ValueError("Storage availability could not be checked.")
    rows = []
    for line in raw.splitlines():
        fields = line.split()
        split = fields.index("-")
        if split < 6 or len(fields) != split + 4:
            raise ValueError("Storage availability could not be checked.")
        point = re.sub(r"\\([0-7]{3})", lambda m: chr(int(m[1], 8)), fields[4])
        rows.append((Path(point), fields))
    return rows


def inspect(steam_value, library_value):
    steam = input_path(steam_value)
    rows = read_mounts()
    used = {}
    required = (STORAGE, STORAGE / "games-external", STORAGE / "roms")
    reserved = (*required, STORAGE / "games-internal", MEDIA, Path("/"))

    def available(path):
        wanted = [p for p in required if beneath(path, p)]
        if beneath(path, MEDIA) and path != MEDIA:
            wanted.append(MEDIA / path.relative_to(MEDIA).parts[0])
        for point in wanted:
            matches = [row for row in rows if row[0] == point]
            if len(matches) != 1:
                raise ValueError("The Steam storage is unavailable or has overlapping mounts.")
            used[str(point)] = matches[0][1]
        covers = [row for row in rows if beneath(path, row[0])]
        if not covers:
            raise ValueError("The Steam storage is unavailable.")
        depth = max(len(row[0].parts) for row in covers)
        covers = [row for row in covers if len(row[0].parts) == depth]
        if len(covers) != 1 or covers[0][0] == Path("/"):
            raise ValueError("The Steam storage is unavailable or ambiguous.")
        point, fields = covers[0]
        if "rw" not in fields[5].split(",") or "rw" not in fields[-1].split(","):
            raise ValueError("The Steam storage is read-only.")
        used[str(point)] = fields

    # FEX/config also use /storage, even when the Steam alias points elsewhere.
    available(STORAGE)

    def probe(path):
        available(path)
        current, pending, entries, links = Path("/"), list(path.parts[1:]), [], 0
        while pending:
            part = pending.pop(0)
            if part in ("", "."):
                continue
            if part == "..":
                current = current.parent
                continue
            candidate = current / part
            if candidate in required or candidate.parent == MEDIA:
                available(candidate)
            try:
                info = candidate.lstat()
            except FileNotFoundError:
                if ".." in pending:
                    raise ValueError("The Steam folder path is ambiguous.")
                resolved = candidate.joinpath(*pending)
                available(resolved)
                if resolved in reserved:
                    raise ValueError("The Steam folder path is ambiguous.")
                if not os.access(current, os.W_OK | os.X_OK):
                    raise ValueError("The Steam folder is not writable.")
                return {"path": str(resolved), "exists": False, "entries": entries}
            entry = [str(candidate), info.st_dev, info.st_ino, info.st_mode]
            if stat.S_ISLNK(info.st_mode):
                links += 1
                if links > 40 or not stat.S_ISDIR(candidate.stat().st_mode):
                    raise ValueError("The Steam folder link is unavailable or invalid.")
                target = os.readlink(candidate)
                if any(ord(c) < 32 for c in target):
                    raise ValueError("The Steam folder link is ambiguous.")
                entry.append(target)
                entries.append(entry)
                target_path = Path(target)
                if target_path.is_absolute():
                    current = Path("/")
                    pending = list(target_path.parts[1:]) + pending
                else:
                    pending = list(target_path.parts) + pending
                continue
            if not stat.S_ISDIR(info.st_mode):
                raise ValueError("A file is blocking the Steam folder.")
            entries.append(entry)
            current = candidate
        available(current)
        if current in reserved or not os.access(current, os.W_OK | os.X_OK):
            raise ValueError("The Steam folder is ambiguous or not writable.")
        return {"path": str(current), "exists": True, "entries": entries}

    root = probe(steam)
    plan = {"steam": steam_value, "library": library_value, "root": root}
    if not root["exists"]:
        library = probe(input_path(library_value))
        a, b = Path(root["path"]), Path(library["path"])
        if beneath(a, b) or beneath(b, a):
            raise ValueError("The Steam folder and library paths overlap.")
        plan["target"] = library
    plan["mounts"] = used
    return plan


def open_directory(path):
    # Use the resolved path and no-follow directory descriptors. mkdir only
    # adds missing directories; neither it nor symlink replaces an existing entry.
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in Path(path).parts[1:]:
            flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
            try:
                child = os.open(part, flags, dir_fd=fd)
            except FileNotFoundError:
                os.mkdir(part, dir_fd=fd)
                child = os.open(part, flags, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


def main():
    mode, steam, library, saved = sys.argv[1:]
    plan = inspect(steam, library)
    if mode == "inspect":
        print(json.dumps(plan, sort_keys=True))
        return
    if mode not in ("verify", "link") or plan != json.loads(saved):
        raise ValueError("The Steam folder or storage changed. Try again when it is available.")
    if mode == "verify" or plan["root"]["exists"]:
        return
    target_fd = open_directory(plan["target"]["path"])
    os.close(target_fd)
    root = Path(plan["root"]["path"])
    parent_fd = open_directory(root.parent)
    try:
        os.symlink(library, root.name, dir_fd=parent_fd)
    finally:
        os.close(parent_fd)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError) as error:
        print("Steam folder check: " + str(error), file=sys.stderr)
        sys.exit(1)
PY_STEAM_ROOT
}

fetch_proton_latest_release() {
  local api_url="$1"
  local asset_pattern="$2"
  local tag_prefix_to_strip="$3"
  local var_prefix="$4"
  local display_name="$5"

  log_info "Fetching latest ${display_name} release from GitHub..."

  local release_json
  release_json=$(curl -fsSL "${api_url}") || die "Failed to fetch ${display_name} latest release info."

  # Extract tag name
  local version_tag
  version_tag=$(echo "${release_json}" | grep -oP '"tag_name":\s*"\K[^"]+' | head -n 1) || die "Failed to parse ${display_name} version tag."
  [ -n "${version_tag}" ] || die "${display_name} version tag is empty."

  # Extract download URL for specified asset pattern, excluding checksums
  local download_url
  download_url=$(echo "${release_json}" | grep -oP '"browser_download_url":\s*"\K[^"]*'"${asset_pattern}"'[^"]*' | grep -v '\.sha512sum' | head -n 1) || die "Failed to parse ${display_name} download URL."
  [ -n "${download_url}" ] || die "Could not find ${asset_pattern} asset in ${display_name} release."

  # Extract filename from URL
  local tar_name
  tar_name=$(basename "${download_url}") || die "Failed to extract ${display_name} filename."
  [ -n "${tar_name}" ] || die "${display_name} filename is empty."

  local version_clean="${version_tag}"
  if [ -n "${tag_prefix_to_strip}" ]; then
    version_clean="${version_tag#${tag_prefix_to_strip}}"
  fi

  # Infer directory name based on tar filename
  local dir_name
  dir_name=$(echo "${tar_name}" | sed 's/\.[^.]*$//' | sed 's/\.[^.]*$//')  # Remove .tar.xz or .tar.gz

  # Set global variables dynamically
  eval "${var_prefix}_VERSION_FULL='${version_clean}'"
  eval "${var_prefix}_TAR='${tar_name}'"
  eval "${var_prefix}_DIR='${dir_name}'"
  eval "${var_prefix}_URL='${download_url}'"

  log_info "${display_name} latest version: ${version_clean}"
  log_info "${display_name} download URL: ${download_url}"
}

ensure_fex_rootfs() {
  log_info "Preparing the Steam support environment. This may take a while..."
  # FEXRootFSFetcher also writes Config.json. Isolate that write, then commit
  # the fully overlaid RootFS and packaged config together. Never clean by glob.
  if /usr/bin/python3 -I -S -B - "${FEX_DATA}" <<'PY_STEAM_FEX'
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import selectors
import shutil
import signal
import stat
import subprocess
import sys
import time

CONFIG = Path("/storage/.config/fex-emu")
DEFAULTS = Path("/usr/config/fex-emu")
OVERLAYS = (
    (Path("/usr/lib/liblsfg-vk-layer.so"), "usr/lib/liblsfg-vk-layer.so"),
    (Path("/usr/share/fex-emu/liblsfg-vk-layer-x86.so"), "usr/lib/liblsfg-vk-layer-x86.so"),
    (Path("/usr/share/vulkan/implicit_layer.d/VkLayer_LSFGVK_frame_generation.json"),
     "usr/share/vulkan/implicit_layer.d/VkLayer_LSFGVK_frame_generation.json"),
    (Path("/usr/share/fex-emu/VkLayer_LSFGVK_frame_generation-x86.json"),
     "usr/share/vulkan/implicit_layer.d/VkLayer_LSFGVK_frame_generation-x86.json"),
)
FETCHER = "/usr/bin/FEXRootFSFetcher"
RESERVE = 256 * 1024 * 1024
MAX_FILE = 2 * 1024 * 1024 * 1024
MAX_TREE = 16 * 1024 * 1024 * 1024
MAX_CONFIG = 64 * 1024 * 1024
MAX_ENTRIES = 250000
FETCH_SECONDS = 900
TOTAL_SECONDS = 1800
ICD = "usr/share/vulkan/icd.d/freedreno_icd.x86_64.json"


def ident(path):
    try:
        info = path.lstat()
    except FileNotFoundError:
        return None
    if not stat.S_ISDIR(info.st_mode):
        raise RuntimeError("FEX replacement requires real directories: " + str(path))
    return [info.st_dev, info.st_ino]


def no_mounts(path):
    boundary = path.absolute()
    for row in Path("/proc/self/mountinfo").read_text().splitlines():
        field = row.split()[4]
        mount = Path(re.sub(r"\\([0-7]{3})", lambda m: chr(int(m[1], 8)), field))
        if mount == boundary or boundary in mount.parents:
            raise RuntimeError("Release mounted FEX paths before refreshing: " + str(path))


def parents(path):
    # No symlinked destination ancestors: do not normalize another storage view.
    for item in reversed((path, *path.parents)):
        if ident(item) is None:
            item.mkdir()
        ident(item)


def capacity(path, required=0):
    info = os.statvfs(path)
    if info.f_bavail * info.f_frsize < RESERVE + required:
        raise RuntimeError("Not enough free space to keep the existing FEX environment.")


def tree_budget(path, limit):
    no_mounts(path)
    total = count = 0
    for base, dirs, files in os.walk(path, followlinks=False):
        for name in dirs + files:
            info = (Path(base) / name).lstat()
            if not (stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode)):
                raise RuntimeError("Unsupported entry in the FEX staging tree.")
            count += 1
            total += info.st_size + 4096
            if info.st_size > MAX_FILE or total > limit or count > MAX_ENTRIES:
                raise RuntimeError("FEX staging exceeds the bounded file/space budget.")
    return total


def inside(root, relative):
    path = root / relative
    target = path.resolve(strict=True)
    if not target.is_relative_to(root.resolve(strict=True)) or not target.is_file():
        raise RuntimeError("Missing or escaping FEX file: " + relative)
    return target


def document(path):
    if path.stat().st_size > 1024 * 1024:
        raise RuntimeError("FEX metadata exceeds its size bound.")
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise RuntimeError("FEX metadata is not a JSON object.")
    return data


def elf(path, machine):
    with path.open("rb") as stream:
        header = stream.read(20)
    if (len(header) != 20 or header[:6] != b"\x7fELF\x02\x01"
            or int.from_bytes(header[18:20], "little") != machine):
        raise RuntimeError("Missing or wrong-architecture FEX binary: " + str(path))


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def validate(root, config):
    ident(root)
    ident(config)
    required = ["usr/bin/env", "usr/lib/ld-linux-x86-64.so.2", "usr/lib/libc.so.6",
                "graphics_provider.json", ICD] + [rel for _, rel in OVERLAYS]
    for rel in required[:3]:
        elf(inside(root, rel), 62)
    if not document(inside(root, "graphics_provider.json")):
        raise RuntimeError("Empty graphics provider description.")
    if document(inside(root, ICD)).get("ICD", {}).get("library_path") != "libvulkan_freedreno.so":
        raise RuntimeError("Freedreno ICD does not select the host driver.")
    elf(inside(root, OVERLAYS[0][1]), 183)
    elf(inside(root, OVERLAYS[1][1]), 62)
    for index, suffix in ((2, ""), (3, "_x86")):
        layer = document(inside(root, OVERLAYS[index][1])).get("layer", {})
        if (layer.get("name") != "VK_LAYER_LSFGVK_frame_generation" + suffix
                or layer.get("library_path") != "/usr/lib/liblsfg-vk-layer" + ("-x86" if suffix else "") + ".so"):
            raise RuntimeError("Invalid LSFG layer description.")
    if document(inside(config, "Config.json")).get("Config", {}).get("RootFS") != "ArchLinux":
        raise RuntimeError("FEX config does not select the prepared ArchLinux tree.")
    packaged = {}
    for base, dirs, files in os.walk(DEFAULTS, followlinks=False):
        for name in dirs + files:
            source = Path(base) / name
            if source.is_symlink():
                raise RuntimeError("Unexpected link in packaged FEX config.")
            if source.is_file():
                rel = str(source.relative_to(DEFAULTS))
                packaged[rel] = digest(inside(config, rel))
                if packaged[rel] != digest(source):
                    raise RuntimeError("Packaged FEX config copy failed validation: " + rel)
    return {"root": {rel: digest(inside(root, rel)) for rel in required}, "config": packaged}


def overlay(root):
    for source, rel in OVERLAYS:
        # A RootFS symlink must never redirect a host-side overlay copy.
        dest = root / rel
        parent = dest.parent.resolve(strict=True)
        if not parent.is_relative_to(root.resolve(strict=True)) or dest.is_symlink():
            raise RuntimeError("Unsafe FEX overlay destination: " + rel)
        if not source.is_file() or source.stat().st_size > MAX_CONFIG:
            raise RuntimeError("Required FEX overlay is missing or oversized: " + source.name)
        shutil.copy2(source, dest)
    for rel, section, key, old, new in (
        (OVERLAYS[3][1], "layer", "name", "VK_LAYER_LSFGVK_frame_generation", "VK_LAYER_LSFGVK_frame_generation_x86"),
        (ICD, "ICD", "library_path", "/usr/lib/libvulkan_freedreno.so", "libvulkan_freedreno.so"),
    ):
        path = inside(root, rel)
        data = document(path)
        if data.get(section, {}).get(key) not in (old, new):
            raise RuntimeError("Unexpected FEX overlay metadata: " + rel)
        data[section][key] = new
        path.write_text(json.dumps(data, indent=2) + "\n")


def config_copy(source, destination):
    # Preserve extra config files, but apply the packaged defaults just as the
    # previous cp -r did. Do not follow any existing config link when overlaying.
    ident(source)
    for base, dirs, files in os.walk(source, followlinks=False):
        relative = Path(base).relative_to(source)
        target = destination / relative
        if target.is_symlink():
            raise RuntimeError("Refusing a linked config overlay directory.")
        target.mkdir(exist_ok=True)
        for name in dirs + files:
            item, out = Path(base) / name, target / name
            if out.is_symlink():
                raise RuntimeError("Refusing a linked config overlay entry.")
            if item.is_symlink():
                if out.exists():
                    raise RuntimeError("Conflicting config link.")
                out.symlink_to(os.readlink(item))
            elif item.is_file():
                if out.exists() and not out.is_file():
                    raise RuntimeError("Conflicting config entry.")
                shutil.copy2(item, out)
        shutil.copystat(base, target)


def fetch_environment(work):
    # No inherited FEX_*, STEAM_COMPAT_*, or loader/config overrides.
    # HOME must exist or FEX falls back to passwd/PWD. Both FEX paths need '/'.
    environment = {"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
            "HOME": str(work / "home"), "PWD": str(work / "home"),
            "TMPDIR": str(work / "tmp"), "XDG_DATA_HOME": str(work / "data"),
            "XDG_CONFIG_HOME": str(work / "fetch-config"), "XDG_CACHE_HOME": str(work / "cache"),
            "FEX_APP_DATA_LOCATION": str(work / "data") + "/",
            "FEX_APP_CONFIG_LOCATION": str(work / "fetch-config") + "/",
            "FEX_APP_CACHE_LOCATION": str(work / "cache") + "/"}
    # Keep the existing transport's explicit proxy settings; never log values.
    for key in ("http_proxy", "https_proxy", "all_proxy", "no_proxy",
                "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY"):
        if key in os.environ:
            environment[key] = os.environ[key]
    return environment


def fetch_rootfs(work):
    # The guardian survives SIGKILL of the updater, holds its inherited flock,
    # and kills the entire fetcher/curl/extractor group on pipe EOF or timeout.
    read_fd, write_fd = os.pipe()
    guardian = os.fork()
    if guardian == 0:
        os.close(write_fd)
        os.setsid()
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGALRM):
            signal.signal(sig, interrupted)
        signal.alarm(0)
        proc = None
        result = 1
        try:
            resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_FILE, MAX_FILE))
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
            proc = subprocess.Popen(
                [FETCHER, "--distro-name=arch", "--distro-version=rolling", "-y", "-x", "--force-ui=tty"],
                cwd=work / "home", env=fetch_environment(work), stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
            deadline = time.monotonic() + FETCH_SECONDS
            next_scan = 0.0
            selector = selectors.DefaultSelector()
            selector.register(read_fd, selectors.EVENT_READ)
            selector.register(proc.stdout, selectors.EVENT_READ)
            logged = 0
            with (work / "fetch.log").open("wb") as log:
                while True:
                    capacity(work)
                    if time.monotonic() >= next_scan:
                        tree_budget(work / "data", MAX_TREE)
                        next_scan = time.monotonic() + 1
                    if time.monotonic() >= deadline:
                        raise RuntimeError("FEX fetch/extraction reached its time limit.")
                    for key, _ in selector.select(0.2):
                        if key.fd == read_fd:
                            raise RuntimeError("FEX updater exited; cancelling its fetcher group.")
                        chunk = os.read(key.fd, 65536)
                        if not chunk:
                            selector.unregister(key.fileobj)
                        else:
                            saved = chunk[:max(0, 65536 - logged)]
                            log.write(saved)
                            logged += len(saved)
                    code = proc.poll()
                    if code is not None:
                        if code != 0:
                            raise RuntimeError("FEX fetcher exited " + str(code))
                        result = 0
                        break
        except BaseException as error:
            print("FEX fetch stopped: " + str(error), file=sys.stderr, flush=True)
        finally:
            for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGALRM):
                signal.signal(sig, signal.SIG_IGN)
            if proc is not None:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    result = 1
            os.close(read_fd)
            os._exit(result)
    os.close(read_fd)
    try:
        _, status = os.waitpid(guardian, 0)
        if os.waitstatus_to_exitcode(status) != 0:
            raise RuntimeError("FEX download or extraction did not finish.")
    finally:
        # On a catchable interruption the guardian sees EOF and kills children
        # before rollback can remove their staging directory. Mask repeated
        # catchable signals while waiting; SIGKILL still leaves the guardian's
        # inherited lock held until its process group has been killed.
        mask = signal.pthread_sigmask(signal.SIG_BLOCK,
                                     {signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGALRM})
        try:
            os.close(write_fd)
            try:
                os.waitpid(guardian, 0)
            except ChildProcessError:
                pass
        finally:
            signal.pthread_sigmask(signal.SIG_SETMASK, mask)


class FexUpdate:
    def __init__(self, data):
        self.data = data
        self.root = data / "RootFS" / "ArchLinux"
        self.config = CONFIG
        parents(self.root.parent)
        parents(self.config.parent)
        self.device = self.data.stat().st_dev
        if self.config.parent.stat().st_dev != self.device:
            raise RuntimeError("FEX root and config must share a filesystem for recovery.")
        self.work = data / ".steam-fex-update"
        self.state = None
        self.check_live()

    def check_live(self):
        for path in (self.root, self.config):
            value = ident(path)
            if value is not None and value[0] != self.device:
                raise RuntimeError("FEX destination is on another filesystem.")
            no_mounts(path)

    def write_state(self):
        pending = self.work / "state.tmp"
        with pending.open("w") as stream:
            json.dump(self.state, stream)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(pending, self.work / "state.json")
        fd = os.open(self.work, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)

    def clean(self):
        no_mounts(self.work)
        for item in self.work.iterdir():
            if item.name == "state.json":
                continue
            if item.is_dir() and not item.is_symlink():
                shutil.rmtree(item)
            else:
                item.unlink()
        (self.work / "state.json").unlink(missing_ok=True)
        self.work.rmdir()
        self.state = None

    def recover(self):
        if ident(self.work) is None:
            return
        no_mounts(self.work)
        journal = self.work / "state.json"
        if not journal.exists():
            # Before first journal publication only this temporary file may
            # exist. After final cleanup the directory may be empty.
            entries = list(self.work.iterdir())
            if entries:
                if len(entries) != 1 or entries[0].name != "state.tmp" or not stat.S_ISREG(entries[0].lstat().st_mode):
                    raise RuntimeError("Unrecognized FEX staging directory; retaining it.")
                entries[0].unlink()
            self.work.rmdir()
            return
        if journal.is_symlink() or not journal.is_file() or journal.stat().st_size > 65536:
            raise RuntimeError("Invalid FEX recovery journal; retaining it.")
        self.state = json.loads(journal.read_text())
        if (self.state.get("format") != 1 or self.state.get("data") != str(self.data)
                or self.state.get("config") != str(self.config)
                or self.state.get("phase") not in ("staging", "prepared", "committed")):
            raise RuntimeError("Unrecognized FEX recovery journal; retaining it.")
        self.check_live()
        phase = self.state["phase"]
        if phase == "committed":
            if (any(ident(getattr(self, name)) != self.state["new"][name] for name in ("root", "config"))
                    or validate(self.root, self.config) != self.state["validation"]):
                raise RuntimeError("Committed FEX environment changed; retaining recovery data.")
        elif phase == "prepared":
            for name in ("config", "root"):
                live = getattr(self, name)
                old, new = self.state["old"][name], self.state["new"][name]
                previous = self.work / ("previous-" + name)
                current = ident(live)
                if current == old:
                    if ident(previous) is not None:
                        raise RuntimeError("Ambiguous FEX recovery copy; retaining it.")
                    continue
                if old is not None and ident(previous) != old:
                    raise RuntimeError("Previous FEX identity changed; retaining recovery data.")
                if current == new:
                    discard = self.work / ("discard-" + name)
                    if ident(discard) is not None:
                        raise RuntimeError("Ambiguous FEX discard path; retaining it.")
                    os.rename(live, discard)
                elif current is not None:
                    raise RuntimeError("FEX destination changed outside this update.")
                if old is not None:
                    os.rename(previous, live)
        self.clean()

    def begin(self):
        self.work.mkdir(mode=0o700)
        self.state = {"format": 1, "data": str(self.data), "config": str(self.config), "phase": "staging",
                      "old": {name: ident(getattr(self, name)) for name in ("root", "config")}}
        self.write_state()
        for name in ("home", "tmp", "data", "cache", "fetch-config", "new-config"):
            (self.work / name).mkdir()

    def stage(self):
        # Inspect required local inputs before allowing a download.
        if ident(DEFAULTS) is None:
            raise RuntimeError("Packaged FEX config is missing.")
        needed = tree_budget(DEFAULTS, MAX_CONFIG)
        if ident(self.config) is not None:
            needed += tree_budget(self.config, MAX_CONFIG)
        capacity(self.work, needed)
        for source, _ in OVERLAYS:
            if not source.is_file() or source.stat().st_size > MAX_CONFIG:
                raise RuntimeError("Required FEX overlay is missing or oversized: " + source.name)
        config = self.work / "new-config"
        if ident(self.config) is not None:
            config_copy(self.config, config)
        config_copy(DEFAULTS, config)
        tree_budget(config, MAX_CONFIG)
        fetch_rootfs(self.work)
        root = self.work / "data" / "RootFS" / "ArchLinux"
        if ident(root) is None:
            raise RuntimeError("Fetcher did not produce an extracted ArchLinux directory.")
        if document(inside(self.work / "fetch-config", "Config.json")).get("Config", {}).get("RootFS") != "ArchLinux":
            raise RuntimeError("Fetcher selected an unexpected RootFS or left an unextracted image.")
        tree_budget(self.work / "data", MAX_TREE)
        overlay(root)
        capacity(self.work)
        self.check_live()
        validation = validate(root, config)
        if any(ident(getattr(self, name)) != self.state["old"][name] for name in ("root", "config")):
            raise RuntimeError("FEX destination changed while preparing its replacement.")
        self.state.update(phase="prepared", new={"root": ident(root), "config": ident(config)}, validation=validation)
        self.write_state()

    def activate(self):
        for name, staged in (("root", self.work / "data" / "RootFS" / "ArchLinux"),
                             ("config", self.work / "new-config")):
            live = getattr(self, name)
            if ident(live) != self.state["old"][name]:
                raise RuntimeError("FEX destination changed before activation.")
            if self.state["old"][name] is not None:
                os.rename(live, self.work / ("previous-" + name))
            os.rename(staged, live)
        if validate(self.root, self.config) != self.state["validation"]:
            raise RuntimeError("Activated FEX environment failed validation.")
        self.state["phase"] = "committed"
        self.write_state()
        self.clean()


def interrupted(signum, frame):
    raise InterruptedError("FEX refresh interrupted by signal " + str(signum))


def main():
    update = FexUpdate(Path(sys.argv[1]))
    fd = os.open(update.data / ".steam-fex-update.lock", os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode) or os.fstat(fd).st_nlink != 1:
            raise RuntimeError("Invalid FEX update lock.")
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGALRM):
            signal.signal(sig, interrupted)
        signal.alarm(TOTAL_SECONDS)
        try:
            update.recover()
            capacity(update.data)
            update.begin()
            update.stage()
            update.activate()
            return 0
        except Exception as error:
            print("FEX refresh failed: " + str(error), file=sys.stderr)
            signal.alarm(0)
            # Do not interrupt rollback with a second catchable termination.
            for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
                signal.signal(sig, signal.SIG_IGN)
            try:
                update.recover()
            except Exception as recovery_error:
                print("FEX recovery data retained at " + str(update.work) + ": " + str(recovery_error), file=sys.stderr)
            return 1
        finally:
            signal.alarm(0)
    finally:
        os.close(fd)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print("FEX refresh refused: " + str(error), file=sys.stderr)
        sys.exit(1)
PY_STEAM_FEX
  then
    log_info "Steam support environment is ready."
  else
    die "The Steam support environment could not be updated. Try Install Steam again."
  fi
}

link_steam_library() {
  log_info "Checking Steam library..."
  steam_root_layout link || die "The Steam library could not be prepared. Installation stopped."
}

ensure_steam_desktop_stub() {
  log_info "Ensuring Steam desktop stub exists..."
  mkdir -p "${APPLICATIONS}"
  touch "${APPLICATIONS}/Steam.desktop" || die "Failed to create Steam.desktop stub."
}

install_steam_runtime_arm64() {
  log_info "Downloading and installing Steam runtime (ARM64)..."
  # Keep the existing runtime until the complete staged archive and both library
  # links validate. The journal also recovers a process killed between renames.
  # This transaction does not cover the separate FEX/client/Proton operations.
  if python3 - "${STEAM}" "${RUNTIME_TAR_VERSION_URL}" "${RUNTIME_TAR_BASE}" <<'PY_STEAM_RUNTIME'
import ctypes
import fcntl
import hashlib
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import re
import resource
import shutil
import signal
import stat
import subprocess
import sys
import tarfile

RUNTIME = "steam-runtime-steamrt-arm64"
LINKS = ("libibus-1.0.so.5", "libva.so.2")
RESERVE = 256 * 1024 * 1024
MAX_ARCHIVE = 2 * 1024 * 1024 * 1024
MAX_EXPANDED = 16 * 1024 * 1024 * 1024
MAX_MEMBERS = 250000
MAX_LINK_BACKUP = 64 * 1024 * 1024


def identity(path):
    try:
        info = path.lstat()
    except FileNotFoundError:
        return None
    if not stat.S_ISDIR(info.st_mode):
        raise RuntimeError("Runtime transaction directory is not a real directory: " + str(path))
    return [info.st_dev, info.st_ino]


def describe(path):
    if path.is_symlink():
        return {"kind": "link", "target": os.readlink(path)}
    if not path.exists():
        return {"kind": "absent"}
    if not path.is_file():
        raise RuntimeError("Refusing to replace a non-file library entry: " + str(path))
    info = path.stat()
    if info.st_size > MAX_LINK_BACKUP:
        raise RuntimeError("Existing library entry exceeds the bounded backup size.")
    return {"kind": "file", "sha256": digest(path), "mode": stat.S_IMODE(info.st_mode),
            "mtime_ns": info.st_mtime_ns}


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def capacity(root, needed):
    if shutil.disk_usage(root).free < needed + RESERVE:
        raise RuntimeError("Not enough free space to keep the previous Steam runtime while replacing it.")


def directory(path, device):
    if path.is_symlink() or not path.is_dir() or path.stat().st_dev != device:
        raise RuntimeError("Runtime update needs real directories on the Steam filesystem: " + str(path))


def no_mounts(path):
    # st_dev alone misses a bind mount on the same filesystem. Never walk a
    # mounted subtree while retiring or rolling back an owned runtime tree.
    boundary = path.resolve()
    for line in Path("/proc/self/mountinfo").read_text().splitlines():
        field = line.split()[4]
        mount = Path(re.sub(r"\\([0-7]{3})", lambda m: chr(int(m[1], 8)), field))
        if mount == boundary or boundary in mount.parents:
            raise RuntimeError("Mounted runtime paths must be released before replacement: " + str(path))


def validate(runtime):
    directory(runtime, runtime.parent.stat().st_dev)
    platforms = list(runtime.glob("steamrt3c_platform_*"))
    if len(platforms) != 1 or platforms[0].is_symlink() or not platforms[0].is_dir():
        raise RuntimeError("Expected one complete Steam ARM64 platform directory.")
    targets = {}
    for name in LINKS:
        matches = list((platforms[0] / "files/lib/aarch64-linux-gnu").glob(name + ".*"))
        if len(matches) != 1:
            raise RuntimeError("Missing or ambiguous runtime library: " + name)
        target = matches[0]
        if not target.resolve(strict=True).is_relative_to(runtime.resolve(strict=True)):
            raise RuntimeError("Runtime library escapes the staged runtime.")
        with target.open("rb") as stream:
            header = stream.read(20)
        if (len(header) != 20 or header[:6] != b"\x7fELF\x02\x01"
                or header[16:20] != b"\x03\x00\xb7\x00"):
            raise RuntimeError("Runtime library is not an ARM64 shared object: " + name)
        targets[name] = {"path": str(target.relative_to(runtime)), "sha256": digest(target)}
    return targets


class RuntimeUpdate:
    def __init__(self, root):
        self.link_root = Path(os.path.abspath(root))
        self.root = root.resolve(strict=True)
        if self.root == Path("/"):
            raise RuntimeError("Refusing the filesystem root as the Steam directory.")
        self.device = self.root.stat().st_dev
        self.work = self.root / ".steam-runtime-update"
        self.live = self.root / RUNTIME
        self.lib = self.root / "lib/aarch64-linux-gnu"
        self.state = None

    def write_state(self):
        pending = self.work / "state.tmp"
        with pending.open("w") as stream:
            json.dump(self.state, stream)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(pending, self.work / "state.json")
        fd = os.open(self.work, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)

    def clean(self):
        # Keep the journal until all other owned remnants are gone. A killed
        # cleanup is retried without accumulating another staging tree.
        for child in self.work.iterdir():
            if child.name == "state.json":
                continue
            if child.is_dir() and not child.is_symlink():
                no_mounts(child)
                shutil.rmtree(child)
            else:
                child.unlink()
        (self.work / "state.json").unlink(missing_ok=True)
        self.work.rmdir()
        self.state = None

    def check_parents(self):
        for path in (self.root / "lib", self.lib):
            if path.exists() or path.is_symlink():
                directory(path, self.device)
                no_mounts(path)

    def recover(self):
        if not self.work.exists() and not self.work.is_symlink():
            return
        directory(self.work, self.device)
        journal = self.work / "state.json"
        if not journal.exists():
            # mkdir can be interrupted before the first journal is written.
            # An empty directory is safe to remove; unknown contents are not.
            self.work.rmdir()
            return
        if journal.is_symlink() or not journal.is_file() or journal.stat().st_size > 65536:
            raise RuntimeError("Refusing an invalid runtime recovery journal.")
        self.state = json.loads(journal.read_text())
        if (self.state.get("format") != 1 or self.state.get("root") != str(self.root)
                or self.state.get("link_root") != str(self.link_root)):
            raise RuntimeError("Unrecognized runtime recovery journal; retaining it.")
        no_mounts(self.work)
        phase = self.state["phase"]
        if phase in ("prepared", "committed"):
            no_mounts(self.live)
            if (set(self.state["targets"]) != set(LINKS)
                    or set(self.state["links"]) != set(LINKS)
                    or any(p not in ("lib/aarch64-linux-gnu", "lib")
                           for p in self.state["created_dirs"])):
                raise RuntimeError("Invalid runtime recovery paths; retaining them.")
            for target in self.state["targets"].values():
                relative = PurePosixPath(target["path"])
                if relative.is_absolute() or ".." in relative.parts or not relative.parts:
                    raise RuntimeError("Invalid runtime recovery target.")
        self.check_parents()
        if phase == "committed":
            if identity(self.live) != self.state["candidate_id"] or validate(self.live) != self.state["targets"]:
                raise RuntimeError("Committed runtime changed; keeping its recovery copy.")
            for name in LINKS:
                if describe(self.lib / name) != self.new_link(name):
                    raise RuntimeError("Committed library link changed; keeping its recovery copy.")
        elif phase == "prepared":
            old_id = self.state["old_id"]
            live_id = identity(self.live)
            backup = self.work / "previous"
            if old_id is not None and live_id == old_id:
                pass  # Not activated yet, or rollback was itself interrupted.
            else:
                if old_id is not None and identity(backup) != old_id:
                    raise RuntimeError("Previous runtime identity changed; no automatic cleanup.")
                if live_id == self.state["candidate_id"]:
                    os.replace(self.live, self.work / "discard")
                elif live_id is not None:
                    raise RuntimeError("Active runtime identity changed; no automatic cleanup.")
                if old_id is not None:
                    os.replace(backup, self.live)
            for name in LINKS:
                saved = self.state["links"][name]
                live = self.lib / name
                current = describe(live)
                if current == saved:
                    continue
                if current != self.new_link(name):
                    raise RuntimeError("Library link changed outside the update; retaining recovery data.")
                if saved["kind"] == "absent":
                    live.unlink()
                else:
                    restore = self.work / ("restore-" + name)
                    restore.unlink(missing_ok=True)
                    shutil.copy2(self.work / ("saved-" + name), restore, follow_symlinks=False)
                    os.replace(restore, live)
            for relative in self.state["created_dirs"]:
                path = self.root / relative
                if path.exists():
                    path.rmdir()  # Never remove another writer's contents.
        elif phase != "staging":
            raise RuntimeError("Unknown runtime recovery phase; retaining it.")
        self.clean()

    def new_link(self, name):
        return {"kind": "link", "target": str(self.link_root / RUNTIME / self.state["targets"][name]["path"])}

    def begin(self):
        self.work.mkdir(mode=0o700)
        self.state = {"format": 1, "root": str(self.root), "link_root": str(self.link_root), "phase": "staging"}
        self.write_state()
        (self.work / "unpack").mkdir()

    def prepare(self):
        candidate = self.work / "unpack" / RUNTIME
        targets = validate(candidate)
        self.check_parents()
        links = {name: describe(self.lib / name) for name in LINKS}
        capacity(self.root, sum((self.lib / name).stat().st_size for name in LINKS
                               if links[name]["kind"] == "file"))
        for name in LINKS:
            if links[name]["kind"] != "absent":
                shutil.copy2(self.lib / name, self.work / ("saved-" + name), follow_symlinks=False)
        old_id = identity(self.live)
        no_mounts(self.live)
        if old_id is not None and old_id[0] != self.device:
            raise RuntimeError("Previous runtime is on a different filesystem.")
        self.state.update(phase="prepared", targets=targets, links=links, old_id=old_id,
                          candidate_id=identity(candidate),
                          created_dirs=[p for p in ("lib/aarch64-linux-gnu", "lib")
                                        if not (self.root / p).exists()])
        self.write_state()  # The complete rollback description precedes every rename.

    def activate(self):
        self.lib.mkdir(parents=True, exist_ok=True)
        if self.state["old_id"] is not None:
            os.replace(self.live, self.work / "previous")
        os.replace(self.work / "unpack" / RUNTIME, self.live)
        for name in LINKS:
            pending = self.work / ("new-" + name)
            pending.symlink_to(self.new_link(name)["target"])
            os.replace(pending, self.lib / name)
        if validate(self.live) != self.state["targets"]:
            raise RuntimeError("Activated runtime failed validation.")
        for name in LINKS:
            if describe(self.lib / name) != self.new_link(name) or not (self.lib / name).is_file():
                raise RuntimeError("Activated runtime library link failed validation.")
        self.state["phase"] = "committed"
        self.write_state()  # Only this point permits retiring the superseded tree.
        self.clean()


def fetch_archive(update, version_url, base_url):
    owner_pid = os.getpid()

    def child_setup(limit=None):
        # SIGKILL cannot run a Python cleanup handler. Linux must kill the
        # transport child with its owner, before another updater can retry.
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.prctl(1, signal.SIGKILL, 0, 0, 0) != 0:  # PR_SET_PDEATHSIG
            raise OSError(ctypes.get_errno(), "Cannot bind downloader lifetime to installer")
        if os.getppid() != owner_pid:  # Parent may have died before prctl.
            os.kill(os.getpid(), signal.SIGKILL)
        if limit is not None:
            resource.setrlimit(resource.RLIMIT_FSIZE, (limit, limit))

    version = subprocess.run(["curl", "-fsSL", "--connect-timeout", "10", "--max-time", "30",
                              "--max-filesize", "128", version_url],
                             check=True, capture_output=True, timeout=35, preexec_fn=child_setup).stdout.decode().strip()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", version):
        raise RuntimeError("Invalid Steam runtime version.")
    capacity(update.root, 1)
    budget = min(MAX_ARCHIVE, shutil.disk_usage(update.root).free - RESERVE)
    archive = update.work / "runtime.tar.xz"

    subprocess.run(["wget", "-t", "3", "-T", "30", "-O", str(archive),
                    base_url + "/" + version + "/" + RUNTIME + ".tar.xz"],
                   check=True, timeout=900, preexec_fn=lambda: child_setup(budget))
    return archive


def unpack_archive(update, archive):
    # Inspect the complete compressed stream (including its integrity footer)
    # before extraction; never use the live Steam directory as tar's destination.
    needed = 0
    seen = set()
    with lzma.open(archive, "rb") as stream:
        with tarfile.open(fileobj=stream, mode="r|") as archive_stream:
            for member in archive_stream:
                path = PurePosixPath(member.name)
                if (path.is_absolute() or ".." in path.parts or not path.parts
                        or path.parts[0] != RUNTIME or path.as_posix() in seen or member.size < 0):
                    raise RuntimeError("Unsafe or duplicate runtime archive path.")
                if not (member.isfile() or member.isdir() or member.issym() or member.islnk()):
                    raise RuntimeError("Unsupported runtime archive entry.")
                seen.add(path.as_posix())
                needed += ((member.size + 4095) // 4096) * 4096 + 8192
                if len(seen) > MAX_MEMBERS or needed > MAX_EXPANDED:
                    raise RuntimeError("Runtime archive exceeds the bounded extraction budget.")
        while True:
            chunk = stream.read(1024 * 1024)
            if stream.tell() > MAX_EXPANDED:
                raise RuntimeError("Runtime archive exceeds the decoded-stream budget.")
            if not chunk:
                break
    capacity(update.root, needed)
    with tarfile.open(archive, "r:xz") as payload:
        payload.extractall(update.work / "unpack", filter="data")
    capacity(update.root, 0)
    archive.unlink()


def interrupted(signum, frame):
    raise InterruptedError("Steam runtime update interrupted by signal " + str(signum))


def main():
    update = RuntimeUpdate(Path(sys.argv[1]))
    # A persistent lock inode serializes this component; never unlink the lock
    # file while another invocation may have opened it. No service is started.
    lock_path = update.root / ".steam-runtime-update.lock"
    fd = os.open(lock_path, os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise RuntimeError("Runtime update lock is not a regular file.")
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGALRM):
            signal.signal(sig, interrupted)
        signal.alarm(1800)
        try:
            update.recover()
            update.check_parents()
            capacity(update.root, 1)
            update.begin()
            archive = fetch_archive(update, sys.argv[2], sys.argv[3])
            unpack_archive(update, archive)
            update.prepare()
            update.activate()
            return 0
        except Exception as error:
            print("Steam runtime replacement failed: " + str(error), file=sys.stderr)
            signal.alarm(0)
            try:
                update.recover()
            except Exception as recovery_error:
                print("Runtime recovery needs attention; previous data is retained at "
                      + str(update.work) + ": " + str(recovery_error), file=sys.stderr)
            return 1
        finally:
            signal.alarm(0)
    finally:
        os.close(fd)


if __name__ == "__main__":
    sys.exit(main())
PY_STEAM_RUNTIME
  then
    return 0
  fi
  die "Steam runtime replacement failed. The installer has stopped."
}

install_steam_client_arm64() {
  if steam_client_state install; then
    return 0
  fi
  die "Steam client setup could not finish. Existing client files were kept."
}

# The first call inspects only the client tree, before profile side effects.
# Support metadata uses STEAM_DOT after profiles, preserving that override.
# A legacy bootstrap check is not native readiness; no old receipt hash is used.
steam_client_state() {
  /usr/bin/python3 -I -S -B - "$1" "${STEAM_ROOT_PLAN}" "${STEAM_DOT:-}" "${STEAM_CLIENT_PLAN:-}" "${STEAM_CLIENT_METADATA_PLAN:-}" <<'PY_STEAM_CLIENT'
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
PY_STEAM_CLIENT
}

install_bundled_proton_files() {
  log_info "Installing bundled Proton files..."
  cp -f "/usr/share/steam/registry.vdf" "${STEAM_DOT}" || die "Failed to copy registry.vdf."
}

install_proton_variant() {
  local display_name="$1"
  # The fifth argument is retained for caller compatibility, never for deletion:
  # games can select an older named version even after a new version installs.
  log_info "Checking and installing ${display_name}; keeping existing versions..."
  if /usr/bin/python3 -I -S -B - "${STEAM}" "$2" "$3" "$4" "$5" <<'PY_PROTON_VARIANT'
import ctypes
import fcntl
import gzip
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import resource
import shutil
import signal
import stat
import subprocess
import sys
import tarfile
from urllib.parse import urlsplit

RESERVE = 256 * 1024**2
MAX_ARCHIVE = 2 * 1024**3
MAX_EXPANDED = 16 * 1024**3
MAX_MEMBERS = 250000
WORK = ".proton-variant-stage"
LOCK = ".proton-variant.lock"
FAMILIES = {"proton-cachyos-*-arm64": (r"proton-cachyos-[A-Za-z0-9._+-]+-arm64", ".tar.xz"),
            "GE-Proton*-aarch64": (r"GE-Proton[A-Za-z0-9._+-]+-aarch64", ".tar.gz")}


def directory(path, device):
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_dev != device:
        raise RuntimeError("Proton installation requires a real directory on the Steam filesystem.")


def no_mounts(path):
    for line in Path("/proc/self/mountinfo").read_text().splitlines():
        field = line.split()[4]
        mount = Path(re.sub(r"\\([0-7]{3})", lambda m: chr(int(m[1], 8)), field))
        if mount == path or path in mount.parents:
            raise RuntimeError("A mounted Proton staging or target path must be released first.")


def capacity(root, needed):
    if shutil.disk_usage(root).free < needed + RESERVE:
        raise RuntimeError("Not enough space to install Proton while keeping existing versions.")


def manifest(path):
    if path.is_symlink() or not path.is_file() or not 0 < path.stat().st_size <= 65536:
        raise RuntimeError("Missing or unsupported Proton manifest.")
    raw = path.read_text(encoding="utf-8")
    tokens, offset = [], 0
    pattern = re.compile(r'\s+|//[^\n]*|"(?:\\.|[^"\\])*"|[{}]')
    for match in pattern.finditer(raw):
        if match.start() != offset:
            raise RuntimeError("Malformed Proton manifest.")
        offset = match.end()
        token = match[0]
        if not token.isspace() and not token.startswith("//"):
            tokens.append(token)
    if offset != len(raw):
        raise RuntimeError("Malformed Proton manifest.")
    index = 0

    def object_value(depth=0):
        nonlocal index
        if depth > 16:
            raise RuntimeError("Proton manifest nesting exceeds the supported format.")
        result = {}
        while index < len(tokens) and tokens[index] != "}":
            key = json.loads(tokens[index])
            index += 1
            if not isinstance(key, str) or key in result or index == len(tokens):
                raise RuntimeError("Malformed or duplicate Proton manifest field.")
            if tokens[index] == "{":
                index += 1
                value = object_value(depth + 1)
                if index == len(tokens) or tokens[index] != "}":
                    raise RuntimeError("Unclosed Proton manifest object.")
                index += 1
            else:
                value = json.loads(tokens[index])
                index += 1
            result[key] = value
        return result

    result = object_value()
    if index != len(tokens):
        raise RuntimeError("Unexpected Proton manifest closing brace.")
    return result


def validate(target, device):
    directory(target, device)
    no_mounts(target)
    tool = manifest(target / "toolmanifest.vdf")["manifest"]
    if tool.get("version") != "2" or tool.get("commandline") != "/proton %verb%":
        raise RuntimeError("Unsupported Proton command manifest.")
    entries = manifest(target / "compatibilitytool.vdf")["compatibilitytools"]["compat_tools"]
    if not isinstance(entries, dict) or len(entries) != 1:
        raise RuntimeError("Expected one Proton compatibility tool.")
    name, entry = next(iter(entries.items()))
    if (not name or "##" in name or not isinstance(entry, dict) or entry.get("install_path") != "."
            or entry.get("from_oslist") != "windows" or entry.get("to_oslist") != "linux"):
        raise RuntimeError("Unsupported Proton compatibility manifest.")
    for relative in ("proton", "filelock.py", "version", "files/bin-arm64/wine", "files/bin-arm64/wineserver"):
        path = target / relative
        resolved = path.resolve(strict=True)
        if not resolved.is_relative_to(target) or not resolved.is_file() or resolved.stat().st_size == 0:
            raise RuntimeError("Missing or escaping required Proton payload: " + relative)
        if relative == "proton" or relative.startswith("files/"):
            if not resolved.stat().st_mode & 0o111:
                raise RuntimeError("Required Proton launcher is not executable: " + relative)
        if relative.startswith("files/"):
            with resolved.open("rb") as stream:
                header = stream.read(20)
            if (len(header) != 20 or header[:6] != b"\x7fELF\x02\x01" or header[18:20] != b"\xb7\x00"
                    or header[16:18] not in (b"\x02\x00", b"\x03\x00")):
                raise RuntimeError("Required Proton payload is not ARM64 ELF: " + relative)


def unpack(archive, stage, name, root, suffix):
    # Validate every member and the compressed footer before extraction. Python's
    # data filter then checks resolved link paths again during extraction.
    members, seen, expanded = [], {}, 0
    opener = lzma.open if suffix == ".tar.xz" else gzip.open
    with opener(archive, "rb") as compressed:
        class BoundedReader:
            count = 0

            def read(self, size):
                data = compressed.read(size)
                self.count += len(data)
                if self.count > MAX_EXPANDED + MAX_MEMBERS * 8192:
                    raise RuntimeError("Proton tar stream exceeds the size bound.")
                return data

        reader = BoundedReader()
        with tarfile.open(fileobj=reader, mode="r|") as bundle:
            for member in bundle:
                path = PurePosixPath(member.name)
                if (path.is_absolute() or ".." in path.parts or not path.parts or path.parts[0] != name
                        or str(path) in seen or member.size < 0 or member.issparse()
                        or not (member.isdir() or member.isfile() or member.issym() or member.islnk())):
                    raise RuntimeError("Unsafe or unsupported Proton archive member.")
                if len(path.parts) == 1 and not member.isdir():
                    raise RuntimeError("Proton archive root must be a directory.")
                if member.issym() or member.islnk():
                    link = PurePosixPath(member.linkname)
                    base = str(path.parent) if member.issym() else ""
                    resolved = PurePosixPath(posixpath.normpath(posixpath.join(base, str(link))))
                    if link.is_absolute() or not resolved.parts or resolved.parts[0] != name:
                        raise RuntimeError("Proton archive link escapes its version directory.")
                    if member.islnk() and seen.get(str(resolved)) != "file":
                        raise RuntimeError("Proton hard link must name an earlier regular file.")
                seen[str(path)] = "file" if member.isfile() else "other"
                expanded += ((member.size + 4095) // 4096) * 4096 + 8192
                members.append(member)
                if expanded > MAX_EXPANDED or len(members) > MAX_MEMBERS:
                    raise RuntimeError("Proton archive exceeds the extraction bound.")
        while reader.read(1024 * 1024):
            pass
    capacity(root, expanded)
    stage.mkdir()
    with tarfile.open(archive, "r:*") as bundle:
        bundle.extractall(stage, members=members, filter="data")


def cleanup(work, lock_info, device):
    if not os.path.lexists(work):
        return
    directory(work, device)
    no_mounts(work)
    children = {path.name for path in work.iterdir()}
    if not children:  # Interrupted before the ownership link or after unlinking it.
        work.rmdir()
        return
    owner = work / "owner"
    info = owner.lstat()
    if (not stat.S_ISREG(info.st_mode) or (info.st_dev, info.st_ino) != lock_info
            or not children <= {"owner", "archive", "unpack"}):
        raise RuntimeError("Unrecognized Proton staging contents; leaving them untouched.")
    for name in ("archive", "unpack"):
        path = work / name
        if path.is_symlink() or path.is_file():
            path.unlink()
        elif path.exists():
            directory(path, device)
            shutil.rmtree(path)
    owner.unlink()  # Ownership anchor is always removed last, for retry after a kill.
    work.rmdir()


def activate(candidate, target):
    # Linux renameat2 refuses any existing target, including a concurrently created
    # empty directory. Never replace a player-owned same-name installation.
    libc = ctypes.CDLL(None, use_errno=True)
    rename = libc.renameat2
    rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    rename.restype = ctypes.c_int
    if rename(-100, os.fsencode(candidate), -100, os.fsencode(target), 1) != 0:
        raise OSError(ctypes.get_errno(), "Could not activate staged Proton without replacing existing data")


def install(root, url, tar_name, name, family):
    pattern, suffix = FAMILIES[family]
    if not re.fullmatch(pattern, name) or tar_name != name + suffix:
        raise RuntimeError("Unsupported Proton family or archive name.")
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise RuntimeError("Proton download requires an HTTPS release URL.")
    root = Path(root).resolve(strict=True)
    if root == Path("/"):
        raise RuntimeError("Refusing the filesystem root as a Steam directory.")
    device = root.stat().st_dev
    directory(root, device)
    fd = os.open(root / LOCK, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size:
            raise RuntimeError("Unsupported Proton installer lock.")
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        work = root / WORK
        lock_info = (info.st_dev, info.st_ino)
        cleanup(work, lock_info, device)
        dest = root / "compatibilitytools.d"
        if not os.path.lexists(dest):
            dest.mkdir()
        directory(dest, device)
        no_mounts(dest)
        target = dest / name
        if os.path.lexists(target):
            try:
                validate(target, device)
            except Exception as error:
                raise RuntimeError("Existing Proton target is incomplete or unsupported; kept untouched: "
                                   + name + ". Resolve that version separately before retrying.") from error
            print("Requested Proton version passes payload checks; keeping it unchanged.")
            return
        capacity(root, MAX_ARCHIVE)
        work.mkdir(mode=0o700)
        try:
            os.link(root / LOCK, work / "owner", follow_symlinks=False)
            archive = work / "archive"
            parent = os.getpid()

            def child_setup():
                libc = ctypes.CDLL(None, use_errno=True)
                if libc.prctl(1, signal.SIGKILL, 0, 0, 0) != 0 or os.getppid() != parent:
                    os._exit(125)
                resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_ARCHIVE, MAX_ARCHIVE))

            subprocess.run(["wget", "-t", "3", "-T", "30", "-O", str(archive), url],
                           check=True, timeout=900, preexec_fn=child_setup)
            if not 0 < archive.stat().st_size <= MAX_ARCHIVE:
                raise RuntimeError("Proton download is empty or exceeds the size bound.")
            unpack(archive, work / "unpack", name, root, suffix)
            candidate = work / "unpack" / name
            validate(candidate, device)
            capacity(root, 0)
            activate(candidate, target)
            print("Proton installed; every existing version has been kept.")
        finally:
            cleanup(work, lock_info, device)
    finally:
        os.close(fd)  # Keep the lock inode: never unlink a lock another caller may hold.


def interrupted(signum, frame):
    raise InterruptedError("Proton installation interrupted; existing versions are kept.")


def main():
    for signum in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGALRM):
        signal.signal(signum, interrupted)
    signal.alarm(1800)
    try:
        install(*sys.argv[1:])
    except Exception as error:
        print("Proton installation stopped: " + str(error), file=sys.stderr)
        return 1
    finally:
        signal.alarm(0)
    return 0


if __name__ == "__main__":
    sys.exit(main())
PY_PROTON_VARIANT
  then
    return 0
  else
    die "Could not install ${display_name}. Existing Proton versions have been kept."
  fi
}

install_proton_cachyos() {
  install_proton_variant \
    "Proton-CachyOS" \
    "${PROTON_CACHYOS_URL}" \
    "${PROTON_CACHYOS_TAR}" \
    "${PROTON_CACHYOS_DIR}" \
    "proton-cachyos-*-arm64"
}

install_proton_ge() {
  install_proton_variant \
    "Proton-GE" \
    "${PROTON_GE_URL}" \
    "${PROTON_GE_TAR}" \
    "${PROTON_GE_DIR}" \
    "GE-Proton*-aarch64"
}

run_steam_first_launch() {
  log_info "Running Steam first launch routine..."
  echo 0 > /proc/sys/fs/binfmt_misc/x86 || true
  echo 0 > /proc/sys/fs/binfmt_misc/box32 || true
  echo 0 > /proc/sys/fs/binfmt_misc/box64 || true

  if [ "${DEVICE_HAS_DUAL_SCREEN}" = "true" ]; then
    swaymsg 'seat seat1 fallback true' || log_info "Swaymsg dual screen setup failed, ignoring."
  fi

  # Allow Steam launch commands to fail cleanly if needed, though they shouldn't
  LD_LIBRARY_PATH="${STEAM}/lib/aarch64-linux-gnu/" "${CLIENT_DIR}/steam" -deckard -exitsteam || log_info "Native Steam execution exited with an error."

  if [ "${DEVICE_HAS_DUAL_SCREEN}" = "true" ]; then
    swaymsg 'seat seat1 fallback false' || log_info "Swaymsg dual screen teardown failed, ignoring."
  fi

  systemctl restart systemd-binfmt || die "Failed to restart systemd-binfmt."
}

# --- Execution ---
# Freeze the checked inputs before profile scripts can run or change the roots.
STEAM_ROOT_PLAN="$(steam_root_layout inspect)" || die "Steam storage is not ready. Nothing was installed."
readonly STEAM STEAM_GAMES_ROOT STEAM_ROOT_PLAN
STEAM_CLIENT_PLAN="$(steam_client_state tree)" || die "Steam client files could not be checked. Nothing was changed."
readonly STEAM_CLIENT_PLAN
source /etc/profile
STEAM_DOT="${STEAM_DOT:-/storage/.steam}"
APPLICATIONS="${APPLICATIONS:-/storage/.local/share/applications}"
FEX_DATA="/storage/.local/share/fex-emu"
FEX_ARCH_ROOT="${FEX_DATA}/RootFS/ArchLinux"
FEX_ARCH_USR_LIB="${FEX_ARCH_ROOT}/usr/lib"
RUNTIME_DIR="${STEAM}/steam-runtime-steamrt-arm64"
CLIENT_DIR="${STEAM}/steamrtarm64"
RUNTIME_TAR_BASE="https://repo.steampowered.com/steamrt3c/images"
RUNTIME_TAR_VERSION_URL="${RUNTIME_TAR_BASE}/latest-public-stable.txt"
STEAM_MANIFEST_URL="https://client-update.fastly.steamstatic.com/steam_client_publicbeta_linuxarm64"
STEAM_CDN="https://client-update.steamstatic.com"
PROTON_CACHYOS_RELEASE_API="https://api.github.com/repos/CachyOS/proton-cachyos/releases/latest"
PROTON_GE_RELEASE_API="https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest"
unset MESA_LOADER_DRIVER_OVERRIDE

steam_root_layout verify || die "Steam storage changed. Installation stopped."
# Profiles may already have written. Metadata refusal preserves their selected
# path and does not claim rollback of profile effects or other transactions.
STEAM_CLIENT_METADATA_PLAN="$(steam_client_state metadata)" || die "Steam support folders could not be checked. Client files were kept."
readonly STEAM_DOT STEAM_CLIENT_METADATA_PLAN
set_kill set "-9 steam FEX"
log_info "Starting Steam Installation Process..."

ensure_fex_rootfs
link_steam_library
ensure_steam_desktop_stub
install_steam_runtime_arm64
install_steam_client_arm64
install_bundled_proton_files
fetch_proton_latest_release "${PROTON_CACHYOS_RELEASE_API}" "arm64" "cachyos-" "PROTON_CACHYOS" "Proton-CachyOS"
install_proton_cachyos
fetch_proton_latest_release "${PROTON_GE_RELEASE_API}" "aarch64" "" "PROTON_GE" "Proton-GE"
install_proton_ge
run_steam_first_launch

echo ""
log_success "Steam setup finished. Start Steam to continue."
