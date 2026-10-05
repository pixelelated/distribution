# Four clean/upgraded boot observations (#383, #441)

Actual tool90675 and all four result channels0. Finished06:43:13; actual06:46:39
owner/watcher/command/all four guest PIDs absent and no QEMU. Exact sourcecf511ce,
ESf6f0, bundle79d56004 and packaged kernel8dfcd6bb independently checked.

Two first-clean16GiB boots at640x480/1280x960 and two COW boots of the actual
RC2-upgraded QA13 disk all match1.0 at unchanged0.995 threshold. Every old-logo,
blank and wrong-resolution negative control rejects. Four actual best frames
were directly reviewed; original full capture hashes/scores are retained.
Only best frames and negative controls are copied into Git; all original
captures remain under the owner with their hashes in artifacts.json.

Clean cmdlines contain quiet; upgraded cmdlines retain their old no-quiet
configuration and thus exercise the installed initramfs fallback. Both include
serial/tty0 consoles and carry the exact expected kernel digest and fullbuildID.
No product or boot configuration was edited. Original upgraded backing and
clean base hashes remain unchanged. This proves the fresh successor consumed
QA13's actual upgraded disk after the retained old dependency failure (#441).
The remaining targeted candidate qualification is still required.
