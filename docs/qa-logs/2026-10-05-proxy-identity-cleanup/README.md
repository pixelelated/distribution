# Proxy identity cleanup (#409, #168)

The maintainer clarified that Rasteratops never became a user-facing OS.
The existing side-conversation change removes only that platform-name alias;
ROCKNIX and pixelelated detection and their shared settings path remain.
Patch018 and the unsubmitted upstream draft receive pixelelated filenames.

Retained host proof: all15 patches apply with zero fuzz,16 existing ROCKNIX
unit cases pass, and direct fixtures accept ROCKNIX/pixelelated and reject the
unshipped name. The receipt verifies the exact one-line patch delta and equal
packaged/contribution patch bytes. No new upstream submission was made.

Replacement08 is immutable and does not contain this change. Complete its
running four-boot repair proof, then publish/freeze replacement09 and qualify
those exact bytes. Its15 remaining sealed owners stay unstarted; new owners
will preserve their assertions and point to the replacement09 input manifest.
