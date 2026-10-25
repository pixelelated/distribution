"""Classify a built kernel config against a committed one, by option name.

Read-only. Prints counts and the changed values (EXTRA_FIRMWARE summarised).
"""
import collections
import re
import sys


def load(path):
    opts = {}
    with open(path, encoding="utf-8", errors="replace") as stream:
        for line in stream:
            line = line.rstrip("\n")
            m = re.match(r"^(CONFIG_[A-Za-z0-9_]+)=(.*)$", line)
            if m:
                opts[m.group(1)] = m.group(2)
                continue
            m = re.match(r"^# (CONFIG_[A-Za-z0-9_]+) is not set$", line)
            if m:
                opts[m.group(1)] = "n"
    return opts


ours, built = load(sys.argv[1]), load(sys.argv[2])
changed = sorted(k for k in ours if k in built and ours[k] != built[k])
gone = sorted(k for k in ours if k not in built)
new = sorted(k for k in built if k not in ours)
print("options ours", len(ours), "built", len(built))
print("changed", len(changed))
print("gone", len(gone), "set", sum(1 for k in gone if ours[k] != "n"))
print("new", len(new), "set", sum(1 for k in new if built[k] != "n"))
for k in changed:
    if k == "CONFIG_EXTRA_FIRMWARE":
        entries = built[k].strip('"').split()
        tops = collections.Counter(e.split("/")[0] for e in entries)
        print("  CHG", k, ours[k], "->", len(entries), "entries", dict(tops.most_common(7)))
    elif k == "CONFIG_INITRAMFS_SOURCE":
        print("  CHG", k, ours[k], "-> (a build path)")
    else:
        print("  CHG", k, ours[k], "->", built[k])
fork = ["FW_CFG_SYSFS", "WATCHDOG", "WATCHDOG_CORE", "WATCHDOG_SYSFS", "I6300ESB_WDT",
        "PSTORE", "PSTORE_COMPRESS", "PSTORE_CONSOLE", "PSTORE_RAM", "EFI_VARS_PSTORE"]
kept = sum(1 for o in fork if ours.get("CONFIG_" + o) == built.get("CONFIG_" + o) == "y")
print("fork settings kept in the build", kept, "of", len(fork))
for k in ("CONFIG_PREEMPT_VOLUNTARY", "CONFIG_PREEMPT", "CONFIG_DRM_AMDGPU", "CONFIG_DRM_RADEON", "CONFIG_DRM_I915", "CONFIG_DRM_VIRTIO_GPU"):
    print(" ", k, "ours", ours.get(k, "absent"), "built", built.get(k, "absent"))
