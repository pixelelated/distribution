#!/usr/bin/env python3
"""T22's reachability and coverage tables, generated, never typed.

    python3 -I -B t22-reach.py <rows.json> <out-dir>

rows.json is the membership block's rows (the brief's § 2 block at
2174265e9c, saved by the stage-A run). For each of the 422 paths the
first matching rule below decides *installed on* (which shipped image
carries the file), *runs on* (where it is executed, sourced or read at
run time) and the deciding line at 8ebaf8daad. The package-level reach
is the inventory's `reachable_by` (H700-aarch64, SM8550-aarch64,
GENERIC_X64-x86_64 -> H700, SM8550, VM). Exits 1 unless the rows sum to
422 and the two figures the brief names (8 install-time rows no shipped
image installs; 213 platform files no shipped device runs) come out.
"""
import collections, json, re, sys

rows = json.load(open(sys.argv[1]))
out = sys.argv[2]
IMG = {"H700-aarch64": "H700", "SM8550-aarch64": "SM8550", "GENERIC_X64-x86_64": "VM"}
SHIP = {"H700": "H700", "SM8550": "SM8550", "GENERIC_X64": "VM"}
P = "projects/ROCKNIX/packages/"
SI = "scripts/install"           # its per-subdirectory copy blocks at 8ebaf8daad (grep -n 'if \[ -d ${PKG_TMP_DIR}/')
SUBDIR = {"profile.d": f"{SI}:86-89", "tmpfiles.d": f"{SI}:91-94", "autostart": f"{SI}:96-100",
          "system.d": f"{SI}:107-110", "udev.d": f"{SI}:112-115", "hwdb.d": f"{SI}:117-120",
          "sleep.d": f"{SI}:122-125", "sleep.d.serial": f"{SI}:127-130", "sysctl.d": f"{SI}:132-135",
          "modprobe.d": f"{SI}:152-155"}
FLAGS = {  # 098-deviceutils' gates, with the values the three shipped devices set (VM: the QEMU entry under quirks/devices, T29's)
    "fancontrol": ("DEVICE_HAS_FAN", "098-deviceutils:7-13", "SM8550 (platforms/SM8550/020-fan_control:9)"),
    "headphone_sense": ("DEVICE_FAKE_JACKSENSE", "098-deviceutils:15-21", "none of the three sets it true (VM false; H700, SM8550 per device, T29's)"),
    "battery_led_status": ("DEVICE_BATTERY_LED_STATUS", "098-deviceutils:31-37", "SM8550 (platforms/SM8550/030-led-control:7)"),
}


def inst(r):
    return ", ".join(sorted({IMG[i] for i in r["reachable_by"] if i in IMG})) or "none"


def rule(r):
    """(installed on, runs on, deciding line, kind)."""
    rel = r["path"][len(P):]
    a = inst(r)
    parts = rel.split("/")
    if rel.endswith("package.mk"):
        return ("— (recipe)", "build", f"{rel}", "recipe")
    if rel.startswith("hardware/quirks/platforms/"):
        plat, rest = parts[3], "/".join(parts[4:])
        runs = SHIP.get(plat, "none")
        how = ("sleep.sh:84 (HW_DEVICE)" if rest.startswith("sleep.d/")
               else "sleep.sh:44 (HW_DEVICE)" if rest == "modules.keep"
               else "its caller's platforms/${HW_DEVICE}/bin path" if rest.startswith("bin/")
               else "autostart:16-28 (HW_DEVICE)")
        if plat == "RK3566" and rest == "bin/volumealign":
            how = "volume-fixup.service, enabled on RK3566 only (quirks/package.mk:25-28)"
        return (a, runs, f"quirks/package.mk:16-18 (copies every platform); {how}", "platform")
    if rel.startswith("hardware/quirks/system.d/"):
        if parts[-1] == "volume-fixup.service":
            return (a, "none", f"{SUBDIR['system.d']}; enabled only when DEVICE=RK3566 (quirks/package.mk:25-28)", "unit")
        return (a, a, f"{SUBDIR['system.d']}; quirks/package.mk:24 (enable_service)", "unit")
    if rel.startswith("hardware/quirks/autostart/"):
        return (a, a, f"{SUBDIR['autostart']} -> /usr/lib/autostart/common; autostart:50-54", "autostart")
    if rel.startswith("hardware/quirks/profile.d/"):
        return (a, a, f"{SUBDIR['profile.d']}; sourced by /etc/profile", "profile")
    if rel.startswith("sysutils/system-utils/"):
        rest = "/".join(parts[2:])
        if rest.startswith("sources/devices/"):
            dev = parts[4]
            on = SHIP.get(dev)
            on = on if on and on in a else "none"
            return (on, on, "system-utils/package.mk:27-29 (only sources/devices/${DEVICE})", "device-file")
        if rest.startswith("sources/autostart/common/"):
            return (a, a, "system-utils/package.mk:14-15; autostart:50-54", "autostart")
        if rest.startswith("sources/autostart/"):
            dev = parts[4]
            on = SHIP.get(dev, "none")
            return (on, on, "system-utils/package.mk:30-34 (only sources/autostart/${DEVICE})", "device-file")
        if rest.startswith("sources/scripts/"):
            name = parts[-1]
            if name in FLAGS:
                flag, line, where = FLAGS[name]
                return (a, where, f"system-utils/package.mk:17-26; started by {line} ({flag})", "script")
            return (a, a, "system-utils/package.mk:17-26", "script")
        if rest.startswith("sources/config/"):
            return (a, "read by fancontrol where it runs (SM8550)", "system-utils/package.mk:39-40 (as /usr/config/fancontrol.conf.sample)", "config")
        if rest.startswith("system.d/"):
            name = parts[-1].replace(".service", "")
            gate = {"video": "098-deviceutils:23-29 (DEVICE_HAS_HDMI; VM true)", "input": "098-deviceutils:39-40 (always)",
                    "fancontrol": "098-deviceutils:7-13 (SM8550)", "headphones": "098-deviceutils:15-21 (DEVICE_FAKE_JACKSENSE)",
                    "batteryledstatus": "098-deviceutils:31-37 (SM8550)"}[name]
            runs = {"input": a, "video": "VM (H700, SM8550 per device: T29's)", "fancontrol": "SM8550",
                    "batteryledstatus": "SM8550", "headphones": "per device (T29's); VM no"}[name]
            return (a, runs, f"{SUBDIR['system.d']}; no .wants link (guest s2c); started by {gate}", "unit")
        sd = parts[2]
        return (a, a, SUBDIR.get(sd, "system-utils/package.mk"), sd)
    if rel.startswith("sysutils/busybox/"):
        rest = "/".join(parts[2:])
        if rest == "config/busybox-host.conf":
            return ("none (the host tool)", "build", "busybox/package.mk:65 (configure_host)", "config")
        if rest == "config/busybox-target.conf":
            return (a, a, "busybox/package.mk:75-76 (compiled into /usr/bin/busybox)", "config")
        if rest == "config/busybox-init.conf":
            return (a, a, "busybox/package.mk:101-102 (the initramfs busybox)", "config")
        if rest.startswith("config/"):
            return (a, a, "busybox/package.mk:141-144", "config")
        if rest in ("scripts/init",):
            return (a, a, "busybox/package.mk:227 (initramfs /init, PID 1)", "script")
        if rest == "scripts/functions":
            return (a, a, "busybox/package.mk:135 and :226", "script")
        if rest == "scripts/getedid":
            return ("VM", "VM", "busybox/package.mk:121 (x86_64 only)", "script")
        if rest.startswith("scripts/"):
            return (a, a, "busybox/package.mk:122-136", "script")
        if rest.startswith("system.d.opt/") or rest.startswith("default.d/"):
            return ("none", "none", "busybox/package.mk:193-201 (CRON_SUPPORT, \"no\" at distributions/ROCKNIX/options:177)", "unit")
        if rest.startswith("sources/console-tools/"):
            return (a, a, "the evtest applet (IF_EVTEST) in /usr/bin/busybox; scripts/init:528 calls it", "c")
        sd = parts[2]
        return (a, a, SUBDIR.get(sd, "busybox/package.mk"), sd)
    if rel.startswith("sysutils/systemd/"):
        rest = "/".join(parts[2:])
        if rest.startswith("scripts/"):
            return (a, a, "systemd/package.mk:231-237", "script")
        if rest.startswith("config/system.conf.d/"):
            return (a, a, "systemd/package.mk:256 and :275 (/etc/systemd/system.conf.d)", "config")
        if rest.startswith("config/"):
            return (a, a, "systemd/package.mk:256 (/usr/config, seeded into /storage/.config at first boot)", "config")
        sd = parts[2]
        return (a, a, SUBDIR.get(sd, "systemd/package.mk"), sd)
    sd = parts[2] if len(parts) > 3 else "sources"
    return (a, a, SUBDIR.get(sd, f"{'/'.join(parts[:2])}/package.mk"), sd)


# What pulls each unit in, at 8ebaf8daad; the .wants links are read on the guest (guest-cycle/s2c-wants.txt).
ALL = "H700, SM8550, VM"
UNIT_RUNS = {
    "led-poweroff.service": (ALL, "multi-user.target.wants (quirks/package.mk:24)"),
    "rocknix-autostart.service": (ALL, "rocknix.target.wants, the default target (rocknix/package.mk:85)"),
    "proc-sys-fs-binfmt_misc.mount": (ALL, "local-fs.target.wants (busybox/package.mk:190)"),
    "var.mount": (ALL, "local-fs.target.wants (busybox/package.mk:189)"),
    "shell.service": ("only when booted with `textmode` on the kernel command line", "textmode.target.wants (busybox/package.mk:187); the target is selected by scripts/init:1215-1216"),
    "textmode.target": ("only when booted with `textmode`", "scripts/init:1215-1216"),
    "show-version.service": (ALL, "basic.target.wants (busybox/package.mk:188)"),
    "storage-log.service": (ALL, "var-log.mount's Requires= (var-log.mount:14)"),
    "var-log.mount": (ALL, "no link; active on the guest (journald's mount dependency on /var/log); ConditionPathExists=!/storage/.cache/volatile-log"),
    "fs-resize.service": ("first boot after a resize request", "fs-resize.target; scripts/init:1363-1364 (/storage/.please_resize_me)"),
    "fs-resize.target": ("first boot after a resize request", "scripts/init:1363-1364"),
    "powerstate.service": (ALL, "multi-user.target.wants (powerstate/package.mk:20)"),
    "debugconfig.service": (ALL, "sysinit.target.wants (guest s2c)"),
    "machine-id.service": (ALL, "sysinit.target.wants (guest s2c)"),
    "systemd-timesyncd-setup.service": (ALL, "sysinit.target.wants (guest s2c)"),
    "usercache.service": (ALL, "sysinit.target.wants (guest s2c)"),
    "userconfig.service": (ALL, "sysinit.target.wants (systemd/package.mk:326)"),
    "network-base.service": (ALL, "network.target.wants (guest s2c)"),
    "udevil-mount@.service": ("when a USB-storage sd* or sr* medium appears", "95-udevil-mount.rules (udevil/package.mk:40)"),
    "fstrim.service": ("only when fstrim.enabled=1 (0 by default)", "fstrim.timer; autostart/sources/daemons/005-fstrim; rocknix system.cfg:55"),
    "fstrim.timer": ("only when fstrim.enabled=1 (0 by default)", "autostart/sources/daemons/005-fstrim; rocknix system.cfg:55"),
}

table = []
for r in sorted(rows, key=lambda r: r["path"]):
    i, ro, line, kind = rule(r)
    base = r["path"].rsplit("/", 1)[-1]
    if base in UNIT_RUNS and kind != "platform" and i != "none" and not ro.startswith("none"):
        ro, why = UNIT_RUNS[base]
        line = f"{line}; {why}"
    table.append({"path": r["path"], "lines": r["lines"], "tier": r["tier"], "language": r.get("language") or "none",
                  "installed": i, "runs": ro, "line": line, "kind": kind})

n = len(table)
not_installed_device = [t for t in table if t["kind"] == "device-file" and t["installed"] == "none"]
plat = [t for t in table if t["kind"] == "platform"]
plat_none = [t for t in plat if t["runs"] == "none"]
runs = collections.Counter(t["runs"] for t in table)
summary = {"rows": n, "platform files": len(plat), "platform files run on no shipped device": len(plat_none),
           "install-time rows no shipped image installs": len(not_installed_device),
           "installed on none": sum(t["installed"].startswith("none") for t in table),
           "recipes (build only)": sum(t["kind"] == "recipe" for t in table),
           "runs on none": sum(t["runs"] == "none" for t in table)}
deltas = []
if n != 422: deltas.append(f"rows {n} != 422")
if len(not_installed_device) != 8: deltas.append(f"install-time rows {len(not_installed_device)} != 8")
if len(plat_none) != 213: deltas.append(f"platform none {len(plat_none)} != 213")
summary["deltas"] = deltas
json.dump({"summary": summary, "rows": table}, open(f"{out}/reach.json", "w"), indent=1)

md = lambda s: str(s).replace("|", "\\|")
with open(f"{out}/reach.md", "w") as f:
    f.write("| Path | Installed on | Runs on | Deciding line (at `8ebaf8daad`) | proved |\n| --- | --- | --- | --- | --- |\n")
    for t in table:
        f.write(f"| `{t['path'][len(P):]}` | {md(t['installed'])} | {md(t['runs'])} | {md(t['line'])} | tree |\n")
with open(f"{out}/coverage.md", "w") as f:
    f.write("| Path | Lines | Tier | Language | Read | proved |\n| --- | ---: | --- | --- | --- | --- |\n")
    for t in table:
        read = ("counted" if t["language"] in ("shell", "recipe", "systemd", "udev", "c")
                else "read, not counted" if t["language"] == "config"
                else "listed (no text)" if t["language"] in ("none", "symlink") else "read")
        f.write(f"| `{t['path'][len(P):]}` | {t['lines'] or 0} | {t['tier']} | {t['language']} | {read} | tree |\n")
print(json.dumps(summary))
sys.exit(1 if deltas else 0)
