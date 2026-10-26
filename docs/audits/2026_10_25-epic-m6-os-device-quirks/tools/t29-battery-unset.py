#!/usr/bin/env python3
"""T29 (#676): what a battery_led_status helper does when led.color was never set,
and after a critical-battery blink.

    python3 -I -B docs/audits/2026_10_25-epic-m6-os-device-quirks/tools/t29-battery-unset.py \
        [--file <battery_led_status>] [--redirect-paths] [--expect unfixed|fixed]

On an SM8550 image, `platforms/SM8550/030-led-control:7` sets
DEVICE_BATTERY_LED_STATUS="true" and `system-utils/sources/autostart/common/
098-deviceutils:31-34` then runs `systemctl start batteryledstatus` at boot;
the unit runs /usr/bin/battery_led_status, and the wrapper execs the device's
bin/battery_led_status. This runs the real script (default: the Nova's at the
worktree) in tools/nova-led-test's shape: settings in a file, sysfs under a
scratch root, `sleep` stubbed to drive the loop.

Cases:
  unset             led.color never set; one pass at 75 % discharging
  rgb               led.color=rgb, the control: the loop must break before writing
  battery           led.color=battery; one pass at 75 % discharging
  critical-recovery led.color=battery; 15 % then 10 % (the five-blink batch) then
                    15 % again, discharging; read after the third pass

--redirect-paths rewrites a helper that hard-codes LED_PATH="/sys/devices/platform/"
and /sys/class/power_supply/battery/ (upstream's copies) to the fixture's paths.
--expect unfixed asserts what the file at 8ebaf8daad does; --expect fixed what
a fixed file must do. Without --expect it prints and exits 0. Writes only under
a temporary directory. Nothing runs on a unit.
"""
from pathlib import Path
import argparse, os, subprocess, sys, tempfile

ap = argparse.ArgumentParser()
ap.add_argument("--file", type=Path,
                default=Path("projects/ROCKNIX/packages/hardware/quirks/devices/Retroid Pocket Nova/bin/battery_led_status"))
ap.add_argument("--redirect-paths", action="store_true")
ap.add_argument("--expect", choices=["unfixed", "fixed"])
a = ap.parse_args()
src = a.file.read_text()
if a.redirect_paths:
    src = src.replace('LED_PATH="/sys/devices/platform/"', 'LED_PATH="${LED_PATH:-/sys/devices/platform/}"')
    src = src.replace("/sys/class/power_supply/battery/", "${BATTERY_PATH}/")

CASES = {"unset": (None, ["75"]), "rgb": ("rgb", ["75"]), "battery": ("battery", ["75"]),
         "critical-recovery": ("battery", ["15", "10", "15"])}
# the sleep stub: a `sleep 15` ends a pass; ten `sleep .5` end a blink batch.
# Either advances to the next capacity; past the last one the script exits.
SLEEP = '''sleep() {
  n=$(cat "$QA_ROOT/step"); halves=$(cat "$QA_ROOT/halves")
  if [ "$1" = ".5" ]; then halves=$((halves + 1)); echo $halves > "$QA_ROOT/halves"; [ $((halves % 10)) -eq 0 ] || return 0; fi
  n=$((n + 1)); echo $n > "$QA_ROOT/step"
  cap=$(sed -n "${n}p" "$QA_ROOT/caps"); [ -n "$cap" ] || exit 0
  echo "$cap" > "$BATTERY_PATH/capacity"
}
'''
res = {}
with tempfile.TemporaryDirectory(prefix="t29-battery-", dir=os.environ.get("TMPDIR")) as t:
    for name, (color, caps) in CASES.items():
        root = Path(t) / name; root.mkdir()
        settings = root / "settings"; settings.write_text("" if color is None else f"led.color={color}\n")
        led = root / "sys"; bat = root / "battery"; bat.mkdir()
        (bat / "capacity").write_text(caps[0] + "\n"); (bat / "status").write_text("Discharging\n")
        (root / "caps").write_text("\n".join(caps) + "\n"); (root / "step").write_text("1\n"); (root / "halves").write_text("0\n")
        dirs = []
        for side in "lr":
            for n in range(1, 5):
                d = led / f"multi-led{side}{n}/leds/rgb:{side}{n}"; d.mkdir(parents=True); dirs.append(d)
                (d / "brightness").write_text("0\n"); (d / "multi_intensity").write_text("0 0 0\n")
        prof = root / "profile"
        prof.write_text('get_setting() { grep -F "$1=" "$QA_SETTINGS" | tail -1 | cut -d= -f2-; }\n'
                        'set_setting() { printf "%s=%s\\n" "$1" "$2" >> "$QA_SETTINGS"; }\n' + SLEEP)
        body = src.replace(". /etc/profile.d/001-functions", f'. "{prof}"').replace(". /etc/profile", f'. "{prof}"')
        script = root / "battery_led_status"; script.write_text(body)
        env = dict(os.environ, LED_PATH=str(led), BATTERY_PATH=str(bat), QA_SETTINGS=str(settings), QA_ROOT=str(root))
        r = subprocess.run(["bash", str(script)], env=env, capture_output=True, text=True, timeout=30)
        b = sorted({(d / "brightness").read_text().strip() for d in dirs})
        m = sorted({(d / "multi_intensity").read_text().strip() for d in dirs})
        lit = b != ["0"]
        res[name] = lit
        print(f"{name}: led.color={color or 'unset'} caps={'>'.join(caps)} rc={r.returncode} brightness={b} multi_intensity={m} lit={'yes' if lit else 'no'}")

want = {"unfixed": {"unset": True, "rgb": False, "battery": True, "critical-recovery": False},
        "fixed": {"unset": False, "rgb": False, "battery": True, "critical-recovery": True}}
if not a.expect:
    print("summary: " + ", ".join(f"{k} lit={'yes' if v else 'no'}" for k, v in res.items()))
    sys.exit(0)
bad = [k for k, v in want[a.expect].items() if res[k] != v]
if bad:
    print(f"t29-battery-unset: UNEXPECTED on {a.expect}: " + ", ".join(bad)); sys.exit(1)
print(f"t29-battery-unset: {a.expect}-expectation-met (" + ", ".join(f"{k} lit={'yes' if v else 'no'}" for k, v in res.items()) + ")")
