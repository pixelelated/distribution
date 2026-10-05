#!/usr/bin/env python3
"""Exercise the real init printk predicate without touching a host console (#433)."""
from pathlib import Path
import json, subprocess, tempfile
root = Path(__file__).resolve().parents[3]
path = 'projects/ROCKNIX/packages/sysutils/busybox/scripts/init'
old = subprocess.check_output(['git', 'show', '57cbc9b981205328444d41f6c4237dc9f5736d7f:' + path], cwd=root, text=True)
new = (root / path).read_text()
cases = [('GENERIC_X64', '', '', True), ('GENERIC_X64', 'yes', '', True),
         ('GENERIC_X64', '', 'yes', False), ('GENERIC_X64', 'yes', 'yes', True),
         ('H700', '', '', False), ('H700', 'yes', '', True),
         ('AMD64', '', '', False), ('AMD64', 'yes', '', True)]
results = []
for label, source in [('old', old), ('new', new)]:
 end = source.index("  echo '1 4 1 7' > /proc/sys/kernel/printk")
 start = source.rfind('\nif ', 0, end) + 1
 block = source[start:source.index('\nfi', end) + 3]
 for device, quiet, debug, expected in cases:
  with tempfile.TemporaryDirectory() as temporary:
   target = Path(temporary) / 'printk'
   target.write_text('unchanged\n')
   script = block.replace('@DEVICENAME@', device).replace('/proc/sys/kernel/printk', '"$1"')
   subprocess.run(['/bin/sh', '-c', script, 'console-policy', str(target)], env={'PATH':'/usr/bin:/bin','QUIET':quiet,'DEBUG':debug}, check=True)
   suppressed = target.read_text() == '1 4 1 7\n'
   assert suppressed == (False if label == 'old' and device == 'GENERIC_X64' and not quiet and not debug else expected)
   results.append({'source':label,'device':device,'quiet':quiet,'debug':debug,'suppressed':suppressed,'meets_fixed_policy':suppressed==expected})
assert sum(not x['meets_fixed_policy'] for x in results) == 1
print(json.dumps({'scope':'isolated real init predicate; no host console write or VM qualification claim','checks':results}, indent=2))
