# Dolphin immutable system-resource repair — #592

The audit found that the package overrides upstream installation and puts Data/Sys
under /usr/config/dolphin-emu, while compiled DATA_DIR makes Dolphin read
/usr/share/dolphin-emu/sys. Frozen image staging has no path or link at that
location. Original startup stderr in the already-retained Dolphin startup packet
contains four fallback badge load failures. The same path serves game settings,
approved achievement settings, fonts, Qt resources and Wii seed data; specific
additional runtime symptoms are not claimed.

The minimal recipe change exposes the existing immutable directory through a
relative symlink at the compiled path. It preserves the copied source resources,
device defaults, launcher configuration and retained /storage data. pkgcheck
passed. There is no new pin, library, Dolphin loader patch or persistent migration.

Source history traces the copy-only layout to inherited9f1fab30f6. The dated
October15 upstream snapshotc17558d2 has the same recipe, while pinned Dolphin's
own CMakeLists already installs Data/Sys to the compiled destination. This is a
ROCKNIX packaging contribution opportunity queued under#585; no submission yet.
The exact independent trace is in the ongoing#590 audit's
finding-dolphin-sys-resources.md. source-readback.json preserves this coordinator's
read-only original path/resource/hash observations.

Can this be done on the VM? Yes. The next engineering image must verify the
actual immutable link and required resource hashes, then its already-planned
three installed Dolphin startup controls must retain original lifecycle/exits
and show none of the four prior badge-load failures. No additional full matrix,
real account or device test is needed for this package defect. Runtime remains
pending; source lint is not installed-image proof. Existing authored homebrew
native gameplay/save qualification remains a separate gate.
