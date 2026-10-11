# USB revision independent of OS version — #531

The shared gadget device revision is now `0x0100` (BCD 1.00). It describes
the USB interface and changes only deliberately with that interface, independently
of semantic release names, dates and source hashes (D-WORKFLOW-160).

## Verified scope

The actual old assignment converts `0.0.1` to `0x0.1` and `0.0.1-dev` to
`0x0.1-`. Both preparation functions write that result to `bcdDevice`;
network preparation uses `set -e`, so rejection can abort normal preparation
before MTP. This calendar assumption predates #530.

`tools/usb-gadget-test` executes the exact shared assignment and complete actual
network/MTP preparation bodies in temporary filesystem fixtures. It does not
source the hardware prologue or dispatch. Nine version values cover calendar,
semantic, prerelease, build metadata, oversized semantic, arbitrary and empty
text: 18 cases and 72 assertions per run. All written attributes and function
links other than the revision match expected existing values, including IDs,
serial, strings, network addresses and MTP's high-speed cap.

The old-source control fails as expected (40/72); corrected host `/bin/sh`,
host Bash and the GENERIC_X64 guest `/bin/sh` each pass 72/72. Guest script
and tool hashes match the reviewed source. The installed old script matches
the retained baseline. Synthetic guest settings and machine identity keep
identical hashes. No personal credentials, saves or cloud contents were used.

The Linux [configfs documentation](https://docs.kernel.org/usb/gadget_configfs.html)
describes the descriptor setup. The upstream
[configfs implementation](https://github.com/torvalds/linux/blob/master/drivers/usb/gadget/configfs.c)
parses bcdDevice as u16 and rejects non-BCD nibbles. This source trace is
separate from our filesystem fixture, which does not simulate kernel rejection.
The exact frozen GENERIC_X64 config disables CONFIG_USB_GADGET; no UDC binding,
enumeration, network traffic or MTP transfer was tested. No UI/pin change is made.

## Original failures and completion

Guest01 stopped before descriptor testing because the harness assumed optional
`/proc/config.gz` existed. All five original result channels remain 1; its
guest was stopped and retired. Guest02 retains that optional probe but uses the
exact frozen source kernel config for the boundary. The source/tool/assertions
were unchanged. All five owner result channels are 0; the old-control test's
intentional 1 remains explicitly recorded. Launcher, runner, watcher, command
and QEMU processes are confirmed absent. Disposable disks, UEFI vars and keys
were removed; compact original evidence remains. Log/text envelopes preserve
the original UTF-8 bytes and their hashes without trimming whitespace.

## Upgrade and qualification boundary

Already written: affected builds could leave incomplete transient configfs
descriptors during preparation; no stored cloud/save/settings migration is
needed. Normal boot preparation reconstructs those transient descriptors.
Other gadget functions and modes are unchanged by the source diff.

This is local implementation review and source-bound host/guest proof, not
an independent release audit or assembled firmware. #531's next-image criterion
stays open: verify the installed script alongside #529/#530 in the combined
candidate and apply the candidate's clean/retained-storage and review gates.
No owner device was contacted and no new firmware build was launched.
