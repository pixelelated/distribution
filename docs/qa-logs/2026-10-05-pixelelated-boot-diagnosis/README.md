# M7.P3 boot console diagnosis (#433, #434)

Candidate57cbc/bundled4007387 remains frozen. UI07's original640x480 match
0.9610208817 against0.995 remains a failure. This directory retains three
bounded diagnostic owners, including both fixture failures. Diagnostic frames
are not replacement-candidate acceptance.

| Owner / actual tool | Result | Observation |
| --- | --- | --- |
| diagnostic01 /84845 | actual and four channels1 | Original boot0.8515924910. Exact consumed initramfs splash copied into guest tmpfs draws1.0. Text-mode console-line erasure lowers match to0.9816916262; graphics-mode write leaves1.0. Intended quiet comparison did not consume quiet: fixture edited GRUB while BIOS used Syslinux. |
| diagnostic02 /75715 | actual and four channels1 | Correct Syslinux edit, then a wrong flat GRUB path stops setup before either quiet comparison. |
| diagnostic03 /7616 | actual and four channels0 | Discovered `/flash/EFI/BOOT/grub.cfg`; both active Syslinux and GRUB modified in disposable COW. Actual quiet/portable/serial/tty0 command-line assertions pass.640x480 and1280x960 both match1.0; all old-logo/blank/wrong-resolution controls reject. |

The diagnostic03 best frames (`018.png` at both sizes) were directly inspected:
intact lowercase Ocean Tiny5 Duo LCD wordmark, black background and separate
version/loading text at the bottom. The diagnostic01 drawn/erased control
frames were also inspected; the erased line visibly cuts through the lettering.
Controlled erasure demonstrates the mechanism; quiet suppresses the boot
console interference in these two observations. We do not identify a particular
kernel message as the sole cause or claim that every noisy boot fails.

All completed owners have actual-tool result custody and verified runner,
watcher and guest teardown. Backing UI07 disk remains SHA256
536638e18ffb498c7e2bc4cc985f876cda47e1265473f25857030b4cca01b9d0.
All raw artifact hashes are retained; selected actual frames, matcher results,
command lines, sanitized kernel journals, before/after configs and launcher
sources are included. The consumed init-only renderer binary remains in the
original owner with its manifest hash; it was not installed on the target root.

## Product correction and upgrade trace

GENERIC_X64's new-image command line adds quiet, preserving both console
arguments. `scripts/mkimage` applies EXTRA_CMDLINE to Syslinux and GRUB. The
init script also applies the existing quiet printk policy to GENERIC_X64 when
not explicitly debugging, because an update preserves an older boot config.
Other devices keep their original predicate. Remove quiet and add debugging for
verbose diagnostics; the serial shell remains independently enabled, and
printk console suppression does not discard kernel journal records.

`check-console-policy.py` executes the real old/new predicate in a temporary
filesystem, with16 observations over clean/retained GENERIC_X64, debug opt-out,
explicit quiet, H700 and AMD64. The old no-quiet GENERIC_X64 case fails the
intended policy; the corrected cases all satisfy it. This is a host control,
not installed boot proof. Shell parsing passes.

Already written: only disposable VM installations have this candidate. Existing
boot and storage settings are retained; the initramfs fallback protects the
upgraded boot without rewriting owner boot configuration. No device or cloud
mutation, renderer change or storage migration is required.

## Next gate

Before the replacement freeze, reconcile #426's newly reported runtime-changing
proxy commits through7252fc. Then build a new immutable candidate and verify
clean and actual RC2-upgraded boots at640x480 and1280x960 using the unchanged
matcher and negative controls, actual serial access and retained kernel logs.
The new initramfs must contain the fallback. Renew required candidate VM tests;
no diagnostic COW or historical candidate result is relabelled as that proof.
#433 stays open until installed replacement acceptance is complete.
