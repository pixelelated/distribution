Checked 2026-10-16. Installed recipe baseline: Sway 1.11, libinput 1.26.2, WebKitGTK 2.54.1. Browser and cloud_oauth are fork-maintained source. WebKitGTK release index and 2.54.1 notes show the selected stable release; no matching Escape fix was identified. Sway issue5423 describes lost events under load on an old 1.4-era stack, with USB resets in one report; this is not evidence for our virtual keyboard case. Its requested kernel/libinput/delivery separation informed the observer, including SYN_DROPPED retention. Search of ROCKNIX browser/Escape did not establish a matching fix. This limited search does not clear all upstream bugs or imply libinput/Sway pins are latest.

https://webkitgtk.org/releases/
https://webkitgtk.org/2026/10/02/webkitgtk2.54.1-released.html
https://github.com/swaywm/sway/issues/5423
