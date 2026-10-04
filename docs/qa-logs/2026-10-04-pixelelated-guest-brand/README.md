# Prepared guest wordmark proof — #344/#409

capture-boot.py retains actual QEMU scanout frames before waiting for the
serial-ready marker. Wired into still-unstarted ui-03 at640x480 and1280x960;
no running tool or frozen product was modified. Captures alone do not pass
branding: match-splash.py subsequently compares every frame against the
approved actual C-renderer reference in the full wordmark bounding rectangle.
The99.5% RGB pixel agreement threshold is fixed before guest execution and
includes transparent LCD gaps rendered black. Outside pixels are unclaimed.

Host controls at both sizes accept the approved reference at100%, reject an
injected retained ROCKNIX logo (about44%), blank (about69–70%) and wrong-size
frames. A complete run containing only the old logo exits1. These are host
controls only; no guest branding verdict exists yet. Original source assets
and guest captures are never changed; injected PNGs are explicit fixtures.
