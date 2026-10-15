# Focused audit UI proof: first attempt

Source packet61bab023 ran in a fresh no-NIC d4af guest at640x480. The four compiled
Wi-Fi controls behaved as expected: baseline observer1 with driver0 and retained
orphan before owned cleanup; candidate explicit/atexit/completed-refresh0 with
no forced cleanup or survivors. These exact worker results are separate from
the incomplete frontend proof.

The GUI navigation failed before opening the picker. Default GENERIC_X64 creates
an extra NETWORK NAME row. Five Down presses selected ENABLE WI-FI; final A
invoked disable. Actual serial calls current/has_ap_mode/disable and the retained
frame agree. No GUI orphan reproduction or candidate GUI/Dolphin frame claim.
The observer deadline remains original2, frontend forced cleanup-9; no survivors.
Root aborted through the existing lifecycle: original outer1, finally-flush0,
QEMUstop0, all host owners absent. Admissione2375d85 consumed failed-investigated.

Exporter0 retained130 guest files and238 original host/source/frame records. Root
rehashed them independently. Abort produced no finish manifest, so the original
lossless_export_verified and guest_manifest_verified remain false. Exported bytes
are retained; no claim of a completed guest inventory is made.

Fresh navigation will bind the conditional row and review the selected network
row before activation. The separately prepared1280 refusal-only packet does not
depend on Wi-Fi navigation. Original sealed/in-flight tools were not changed.

The native-state and next-image source archives are separately marked UNRUN.
Native-state seal e7326fe6 has independent source review and root static0; actual
future-image binding/runtime remain due. Next-image seal60504501 awaits root
review and final committed source binding. Canonical stamp invalidation requires
ordinary Dolphin rebuild even for script changes; no stamp bypass is proposed.
