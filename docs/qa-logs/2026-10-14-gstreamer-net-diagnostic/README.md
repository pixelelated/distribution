# Installed GStreamer dependency failure

Final image d6a87f05c193 includes four gst-plugins-good modules that require
libgstnet-1.0.so.0, but the project recipe removes that runtime library.
The installed UI attempt stopped before browser screens. It returned1 after
an otherwise successful gst-inspect invocation emitted plugin-load warnings;
its fixture failed to persist raw stderr before asserting. That original
failure remains failed.

The bounded no-NIC retained-state diagnostic recovered the exact warning:
adaptivedemux2, rtpmanager, rtsp and udp each fail to load solely because the
library is absent. Original ldd/browser, ldd/scanner and gst-inspect waits are0;
the overall warning check is1. Protected backing disk and selected synthetic
settings remain equal; all owners exited normally, with no cleanup error.
The retained diagnostic's registry and command output are preserved. The old
UI registry is not claimed inspected; its original failure records remain.

Current upstream ROCKNIX project override already preserves all runtime
libraries, although its generic recipe removes controller and net. Our narrow
fix removes the explicit net deletion introduced while repairing controller
packaging under #572, restoring upstream project install behavior. No new
upstream submission is needed for that deletion. Package lint passes, but the
corrected assembled image still needs default-loader/fresh/retained proof and
remaining UI qualification. No RC status or browser-speed cure is claimed.
