# Installed software-rendered boot qualification

Frozen source `d6e8390c93bed87efe2dcc23cd402a271cacd1c7`, bundle `1c69bcf5ab6ebdc3e893a6a989545ac7a23359f0e07baef4e9c2beaca94c52b4`.

All four clean/actual-RC2-upgraded boots at640x480 and1280x960 pass.
Exact wordmark agreement is1.0 against unchanged0.995 acceptance; all12
old-logo, blank and wrong-size negative controls reject. Each boot proves
that the installed service automatically selected Pixman for the actual
software virtio GPU. No runtime renderer override was supplied.

All four best frames were directly reviewed (visual-review.json). Original
raw captures remain in the immutable owner; artifacts.json hashes all791
artifacts and42public artifacts are retained here. Actual QA14 upgraded
backing remains unchanged. The clean disks and COW upgrade disks are separate.

Durable completion20:12:13UTC; all four result channels0. Actual host cleanup
at20:12:47 verifies all eight owner/guest PIDs absent and no QEMU. See
completion.json. These are boot/splash checks; browser and broader renderer
regressions remain separate. Refs #447, #383, #409.
