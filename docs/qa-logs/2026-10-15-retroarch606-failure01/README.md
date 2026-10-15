# RetroArch606 first attempt: fixture failure preserved

Original run20261015T221538Z-05925cbc ended with command/runner/launcher/VM1,
monitor0. The untouched first-boot gate and reviewed empty manager passed.
The sole normal launch returned HTTP200, then the fixture rejected
`actual-gambatte` before any slot/save/quit input. It wrongly required the core
path to resolve directly into /usr/lib/libretro, while unchanged runemu302 uses
/tmp/cores and the installed tmp-cores.mount is an overlay. That mount does not
resolve as a symlink into its lowerdir. Actual launch argv was not retained before
the assertion, a diagnostic limitation corrected prospectively in packet02.

No firmware save defect is demonstrated and no save proof is claimed. The exact
VM teardown passed with no survivors/cleanup errors; original failed result is
consumed as failed-investigated9c03ac9d981a4e6c942b53d9bf5f3d53. The185-member
compact archive/manifest was independently byte-verified by root before custody.
Any fresh attempt uses a distinct owner and packet; this result stays failed.
