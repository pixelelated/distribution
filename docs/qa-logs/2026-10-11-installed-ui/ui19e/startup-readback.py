from ui import *
art=P/'artifacts'
# Read-only current and preceding clean-image boot records from the same disk.
for tag,cmd in [('boots','journalctl --list-boots --no-pager'),('clean-startup','journalctl -b -1 -u essway -u sway --no-pager -o short-monotonic'),('retained-startup','journalctl -b 0 -u essway -u sway --no-pager -o short-monotonic'),('startup-current','systemctl show essway -p ActiveState -p SubState -p NRestarts -p ExecMainStatus -p ExecMainStartTimestampMonotonic; cat /usr/lib/systemd/system/essway.service; sha256sum /usr/bin/sway-ready; cat /etc/os-release')]:
 text=guest(cmd+" | grep -v -i -E 'key|pass|token|user|psk'")
 (art/(tag+'.txt')).write_text(text+'\n')
 if tag in ('clean-startup','retained-startup'):assert 'wayland not available' not in text.lower() and 'Failed to start' not in text and 'Scheduled restart job' not in text
print('PASS read-only clean/retained startup journal; no SDL start failures or automatic retry',flush=True)
