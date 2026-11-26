# Offline RetroAchievements lifecycle checks (#1465)

Read against round `26bc845d9ff213746adeaf83519022020b07e1d5` and the round
image's patched client `40201a2a5d9103223d8c81cef5b4d283cd16ab47`. The rows
follow `scripts-suite-round-9.FAIL.txt` in order. The host's exit 127 occurred
at the absolute lifecycle exec, before a settings write or stop decision. D36
failed before binding a socket because its sandbox had a read-only `/run`.
Neither observation decides the product property (D-QA-065).

In the table, shell tool names refer to the round's `raofflineproxy/sources/`,
Python modules to the patched client's `linux/raofflineproxy/`, and host test
line numbers to the round's `tools/last-good-scripts-test`.

| Host check | Property guarded | Current source | Verdict | Reading and guest assertion |
| --- | --- | --- | --- | --- |
| #186 PL-30, scan, line 2597 | Disable succeeds during a library scan, ends its helper within 10 s, and reports that it stopped. | `raofflineproxy-ctl:274`, `:1850`, `:2323`; `raofflineproxy-cache-indexed:145`; `lifecycle.py:216`; `lifecycle_owner.py:120`, `:366` | **(c)** | The scan and its helper hold shared admission. Disable requires exclusive admission and returns 75 on a verified BUSY outcome without publishing a stop request. This is the cooperative stop design in `0282367b4a` and `e9d4eb544c` under D-RA-050. The guest control expects BUSY with a live writer and the same service PID. |
| #186 PL-30, toggle and stamp, line 2598 | Disable turns the toggle off and the interrupted scan leaves no completion stamp. | `lifecycle_owner.py:120`, `:130`; `raofflineproxy-ctl:1680`, `:1955`; `lifecycle_systemd.py:510` | **(c)** | Under the same D-RA-050 admission design (`0282367b4a`), a busy disable leaves the toggle on. Work may finish normally and publish its real result. The control observes unchanged flags and marker while the image pass is held, then proves an idle disable clears the toggle. |
| #258 PL-013, images, line 2637 | Disable interrupts the image helper and removes its progress record. | `raofflineproxy-ctl:1791`, `:2323`; `raofflineproxy-cache-images:275`; `lifecycle.py:219` | **(c)** | Shared admission deliberately makes disable refuse the live helper (`0282367b4a`, D-RA-050). The images EXIT trap still owns progress cleanup. The guest checks `route=images`, sees BUSY leave it intact, and releases the helper to prove the progress record is removed. |
| #258 PL-013 companion, refresh, line 2678 | Disable interrupts refresh and removes its progress record. | `raofflineproxy-ctl:1833`, `:2323`; `raofflineproxy-refresh:116`; `lifecycle.py:219` | **(c)** | Refresh holds the same shared admission as images. Its own EXIT trap removes the progress record. Disable refuses while it is busy under `0282367b4a` and D-RA-050. The guest drives the common gate through images. |
| #308 gpt F-RA-11, line 7219 | Disable returns in under 5 s even if a scan is waiting for a foreground image helper. | `raofflineproxy-ctl:1744`, `:1761`, `:1955`, `:2323`; `lifecycle_owner.py:120` | **(c)** | The scan still backgrounds the helper so a signal to the scan can interrupt its wait. Disable no longer sends that signal. It refuses the held admission by design (`0282367b4a`, D-RA-050). There is no five-second successful stop contract for a busy pass. |
| #308 gpt F-RA-18, failed hardcore write, line 7660 | An unsuccessful settings write preserves `hardcore_was` and cannot be reported as a successful disable. | `raofflineproxy-lifecycle-settings:24`, `:33`, `:41`; `001-functions:567`; `lifecycle_systemd.py:510`; `lifecycle_observe.py:242` | **(a)** | All three flags are compared and replaced together under the settings lock. A write failure before the rename keeps the record along with the other flags. Completion requires a readback. The old exit 1 is no longer a stable CLI verdict. An unresolved operation returns 2, and a verified recovery in the same invocation can return 0. The guest forces one write failure and checks the original rc 1, the recovery's verified commit, the restored hardcore value, and removal of the saved key after success. |
| #308 gpt F-RA-18, retry, line 7662 | After the write becomes possible, another disable can restore the value from the saved record and remove it. | `lifecycle_owner.py:168`, `:244`, `:299`; `lifecycle_observe.py:240`, `:270` | **(b)** | `ExecStopPost` retries the same commit once. If that also fails, the owner records FAILED and leaves the stopping transition. The observer never yields a terminal outcome for FAILED, and a new disable is refused even after the settings become writable. A settled failure needs a verified way to resume the same commit from the retained record, or to restore normal service and allow a fresh disable. |
| #308 gpt F-RA-18, failed toggle clear, line 7667 | A failed off write leaves the enabled preference, recovery record, marker and running service coherent. The old test expected no service stop at all. | `lifecycle_owner.py:47`, `:79`, `:168`; `lifecycle_systemd.py:510`, `:520` | **(b)** | The new order stops the service cooperatively before committing the flags. If both commit attempts fail, the atomic write retains the enabled preference, marker and saved value but leaves the service down. The failure path should restore the service under the original verified preference or recover the off transaction before reporting a settled result. It cannot report the enabled state as intact while the service is absent. |
| claude G2-D-01 / S-26, ctl, line 12942 | The installed ctl sees the listener the actual service owns. | `raofflineproxy.service:33`, `:40`; `raofflineproxy-ctl:810`, `:824`; `lifecycle_systemd.py:121` | **(a)** | The unit still runs `listening --wait 30`; the lifecycle additionally requires a listener belonging to the exact service PID. The guest enables the unit, runs installed `listening`, and checks the listener inode against the unit's descriptors. |
| claude G2-D-01 / S-26, PPSSPP, line 12943 | PPSSPP's listener reader recognizes that same socket. | `cheevos_ppsspp.sh:77`, `:93`; `raofflineproxy-ctl:810` | **(a)** | PPSSPP uses the same IPv4-reachable address forms as the ctl. With the service enabled and hardcore off, the guest executes the installed reader against real `/proc/net`. There is no need to launch a game or write emulator settings. |
| claude G2-D-01 / S-26, address family, line 12944 | The proxy owns an IPv4 listener on 8080 and no IPv6 listener on that port. | `config.py:30`, `:127`; `boot.py:32`, `:58`; `proxy_service.py:270`; `lifecycle_systemd.py:133` | **(a)** | The prebind and adopted sockets use `AF_INET`, and the fallback server uses the standard IPv4 family. The guest proves that the unit's `MainPID` owns `127.0.0.1:8080` in LISTEN state and owns no listener on 8080 in `tcp6`. |

**Total** · 4 kept, 2 defects, 5 superseded by cooperative busy refusal.

The retry and coherence defects share a single path. A failure before the
settings rename leaves the original enabled preference in place. A failure
after an actual successful rename needs readback and forward completion, so
unconditional restart would also be wrong. The selected recovery must use
the held transition, the exact service epoch and marker, and the verified
flags to choose which completion applies. Tests for persistent write failure
need a disposable guest because the round can retain an unresolved barrier.

## Guest proof

Can this be done on the VM? **Yes.** The installed service, owner and socket
readers, a temporary settings-write fault, and shared cache admission are all
available on the GENERIC_X64 QA image. This lane prepared the test on the
host. The guest verdict is pending.

Run `tools/raofflineproxy-lifecycle-test --port 10022 --identity <qa-key>` on
a quiet, disposable QEMU QA guest. The test uses the installed ctl bytes via
a symlink in `/tmp` because the ctl looks for its helper beside its invocation
path (`raofflineproxy-ctl:1573`). A delayed image helper waits for the test's
release and proves it inherited the actual admission descriptor. A private
mount and network namespace supplies synthetic settings to the images
invocation. Its narrowly scoped `BASH_ENV` answers only the reachability
probe. The image pass still uses the installed ctl's real `images` verb,
both lock inodes, the progress record and the normal helper wait. The disable
request and service run in the guest's ordinary namespaces.

The write fault is a temporary symlink at the settings writer's scratch
path. The real writer rejects and removes it, leaving the original file
intact and allowing `ExecStopPost` to retry. A first writer rc 1, a second
writer rc 0, and the final readback prove that recovery used the original
three flags. The test leaves the persistent failure cases above for a
separate run with a recovery plan.
