# H700 launch admission refusal — original failed result

The October 15 first build attempt stopped before the main build container. The
wrapper removed PROJECT/DEVICE/ARCH before the nested Docker gateway. The existing
plan correctly admitted ROCKNIX/H700 arm and aarch64; its guard refused the absent
triple. Eight normal AArch64 package cleans completed first. No firmware was built.

Original command/runner/launcher returned 2; monitor returned 0. Recorded owners
exited and the named main container, CID file and container-gate receipt were
absent. Ordinary frozen admission consumption recorded failed-investigated, kept
all output holds and deleted zero bytes. These files preserve originals; the
future retry has a new owner and explicit target environment, with unchanged
product and guard bytes. Both device wrapper templates require that correction.

Original cache checksum/inode acceptance remains historical and valid. Current
roots additionally reflect the recorded normal cleanup; no new cache-equality
claim is made. See investigation.json and the original console. #555 owns the
correction and subsequent build/acceptance. This is separate from the completed
#590/#596 product audit; no original audit score or result is changed.
