#!/usr/bin/env python3
"""T29 (#676): what the Nova's battery_led_status does at boot when led.color was never set.

    python3 -I -B docs/audits/2026_10_25-epic-m6-os-device-quirks/tools/t29-battery-unset.py [--file <battery_led_status>]

batteryledstatus.service (system-utils/system.d, WantedBy=multi-user.target)
starts /usr/bin/battery_led_status at every boot, and the wrapper execs the
device's bin/battery_led_status. This runs the real script (default: the
Nova's at the worktree) in tools/nova-led-test's shape: settings in a file,
sysfs under a scratch root, `sleep` stubbed to end the loop after its first
pass. Cases: led.color unset, set to `rgb` (the control: the loop must break
before writing), set to `battery`. One line per case, then a summary.
Writes only under a temporary directory. Nothing runs on a unit.
"""
from pathlib import Path
import argparse, os, subprocess, tempfile

ap = argparse.ArgumentParser()
ap.add_argument("--file", type=Path,
                default=Path("projects/ROCKNIX/packages/hardware/quirks/devices/Retroid Pocket Nova/bin/battery_led_status"))
a = ap.parse_args()
src = a.file.read_text()
cases = [("unset", None), ("rgb", "rgb"), ("battery", "battery")]
out = []
with tempfile.TemporaryDirectory(prefix="t29-battery-", dir=os.environ.get("TMPDIR")) as t:
    for name, color in cases:
        root = Path(t) / name; root.mkdir()
        settings = root / "settings"; settings.write_text("" if color is None else f"led.color={color}\n")
        led = root / "sys"; bat = root / "battery"; bat.mkdir()
        (bat / "capacity").write_text("75\n"); (bat / "status").write_text("Discharging\n")
        dirs = []
        for side in "lr":
            for n in range(1, 5):
                d = led / f"multi-led{side}{n}/leds/rgb:{side}{n}"; d.mkdir(parents=True); dirs.append(d)
                (d / "brightness").write_text("0\n"); (d / "multi_intensity").write_text("0 0 0\n")
        prof = root / "profile"
        prof.write_text('get_setting() { grep -F "$1=" "$QA_SETTINGS" | tail -1 | cut -d= -f2-; }\n'
                        'set_setting() { printf "%s=%s\\n" "$1" "$2" >> "$QA_SETTINGS"; }\n'
                        'sleep() { exit 0; }\n')
        script = root / "battery_led_status"
        script.write_text(src.replace(". /etc/profile", f'. "{prof}"'))
        env = dict(os.environ, LED_PATH=str(led), BATTERY_PATH=str(bat), QA_SETTINGS=str(settings))
        r = subprocess.run(["bash", str(script)], env=env, capture_output=True, text=True, timeout=20)
        b = sorted({(d / "brightness").read_text().strip() for d in dirs})
        m = sorted({(d / "multi_intensity").read_text().strip() for d in dirs})
        lit = b != ["0"]
        out.append((name, r.returncode, b, m, lit))
        print(f"led.color={name}: rc={r.returncode} brightness={b} multi_intensity={m} lit={'yes' if lit else 'no'}")
unset, rgb, battery = out
print("summary: unset lit=%s, rgb lit=%s (control), battery lit=%s" % (
    "yes" if unset[4] else "no", "yes" if rgb[4] else "no", "yes" if battery[4] else "no"))
