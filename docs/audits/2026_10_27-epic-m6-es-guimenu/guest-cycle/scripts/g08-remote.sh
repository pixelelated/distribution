#!/bin/sh
# T26 (#673) G08: a WebDAV remote to a dead local port, no credential, made active.
mkdir -p /storage/.config/rclone
ls -l /storage/.config/rclone/rclone.conf 2>&1 | cut -c1-60
printf '[t26dead]\ntype = webdav\nurl = http://127.0.0.1:9/\nvendor = other\n' > /storage/.config/rclone/rclone.conf
/usr/bin/cloud_remote select t26dead; echo "select rc $?"
/usr/bin/cloud_remote active; echo "active rc $?"
timeout 60 /usr/bin/cloud_setup --check >/dev/null 2>&1; echo "check rc $?"
