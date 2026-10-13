#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
# Copyright (C) 2026-present ROCKNIX (https://github.com/ROCKNIX)
"""Read-only dependency census for #576; no configure, compiler, or guest launch.

Exit 0: declared development prerequisites found (NOT build/runtime acceptance).
Exit 2: missing/old prerequisite. Exit 1: unreadable or unexpected source input.
Only the explicitly supplied sysroot is inspected; host pkg-config is not used.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

# GTK 4.24.1 meson.build, plus the proposed WebKit6/sandbox development pair.
REQUIRED = {
    "glib-2.0": "2.89.3", "gio-2.0": "2.89.3", "gobject-2.0": "2.89.3",
    "gmodule-2.0": "2.89.3", "pango": "1.58", "pangoft2": "1.58",
    "pangocairo": "1.58", "cairo": "1.18.2", "cairo-gobject": "1.18.2",
    "harfbuzz": "8.4.0", "harfbuzz-subset": "8.4.0", "fribidi": "1.0.6",
    "gdk-pixbuf-2.0": "2.30.0", "epoxy": "1.4", "xkbcommon": "0.2.0",
    "wayland-client": "1.24.0", "wayland-protocols": "1.48", "wayland-egl": "0",
    "libpng": "0", "libtiff-4": "0", "libjpeg": "0", "libdrm": "0",
    "graphene-gobject-1.0": "1.10.0", "libsoup-3.0": "3.0.0",
    "gtk4": "4.24.1", "webkitgtk-6.0": "2.54.1", "libseccomp": "0",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def version(text):
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)*", text):
        raise ValueError("unrecognized pkg-config version: " + text)
    return tuple(int(x) for x in text.split(".")) + (0,) * (8 - len(text.split(".")))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sysroot", type=Path, required=True)
    parser.add_argument("--webkit-source", type=Path, required=True)
    args = parser.parse_args()
    root = args.sysroot.resolve(strict=True)
    source = args.webkit_source.resolve(strict=True)
    options = source / "Source/cmake/OptionsGTK.cmake"
    if "SET_PROJECT_VERSION(2 54 1)" not in options.read_text():
        raise ValueError("this census is bound to WebKit2.54.1")
    modules = []
    for name, minimum in REQUIRED.items():
        paths = [root / "usr" / part / "pkgconfig" / (name + ".pc")
                 for part in ("lib", "lib64", "share")]
        found = [p for p in paths if p.is_file()]
        row = {"module": name, "minimum": minimum, "status": "MISSING"}
        broken_links = [p for p in paths if p.is_symlink() and not p.exists()]
        if broken_links:
            row.update(status="BROKEN_SYMLINK", symlink_targets=[
                {"path": str(p.relative_to(root)), "target": str(p.readlink())}
                for p in broken_links])
        if len(found) > 1:
            raise ValueError("ambiguous pkg-config module: " + name)
        if found:
            path = found[0]
            match = re.search(r"^Version:\s*(\S+)\s*$", path.read_text(), re.M)
            if not match:
                raise ValueError("missing literal version: " + str(path))
            actual = match[1]
            row.update(path=str(path.relative_to(root)), version=actual, sha256=digest(path))
            row["status"] = "PRESENT" if version(actual) >= version(minimum) else "TOO_OLD"
            if name in ("gtk4", "webkitgtk-6.0") and actual != minimum:
                row["status"] = "WRONG_EXPERIMENT_VERSION"
        modules.append(row)
    flags = {}
    caches = list(source.glob(".*/CMakeCache.txt"))
    if len(caches) > 1:
        raise ValueError("multiple WebKit build configurations; inspect separately")
    if caches:
        selected = {"USE_GTK4", "ENABLE_BUBBLEWRAP_SANDBOX", "ENABLE_GPU_PROCESS",
                    "ENABLE_SAMPLING_PROFILER", "USE_SYSPROF_CAPTURE", "USE_SKIA",
                    "USE_GSTREAMER_GL", "USE_GBM", "ENABLE_WAYLAND_TARGET", "ENABLE_X11_TARGET"}
        for line in caches[0].read_text().splitlines():
            m = re.fullmatch(r"(\w+):BOOL=(ON|OFF)", line)
            if m and m[1] in selected:
                flags[m[1]] = m[2]
    ready = all(row["status"] == "PRESENT" for row in modules)
    print(json.dumps({
        "evidence_level": "source-and-development-metadata-only",
        "sysroot": str(root), "webkit_source": str(source),
        "webkit_options_sha256": digest(options), "existing_webkit_flags": flags,
        "modules": modules, "prerequisites_present": ready,
        "not_checked": ["ELF link closure", "native build tools", "sandbox executables/kernel/runtime",
                        "GTK4 input port", "installed image", "VM functions or renderer", "memory benefit"],
    }, indent=2))
    return 0 if ready else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print("preflight input error: " + str(error), file=sys.stderr)
        sys.exit(1)
