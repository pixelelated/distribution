# Stopped-media retirement: verification refusal and administrator readback

No media was retired. Ordinary verification stopped at unreadable host process
fields, and the subsequent administrator readback failed before its reader ran
because authentication required a terminal. This packet preserves both original
failures, the exact source and root review, and an unrun terminal continuation.

The completed Steam proof remains independently retained at
[Steam artifact bridge runtime](../2026-10-15-steam-artifact-bridge-runtime/README.md).
The superseded H700 scratch belongs to the separately preserved
[failed selected-state read](../2026-10-15-device-refresh/state-failure03/README.md)
and [accepted H700 continuation](../2026-10-15-device-refresh/h70004/README.md).
None of the five media payloads, firmware, or VM disks is duplicated here.

## Original outcomes

- Verify run `20261015T100631Z-25a99dcd`: original command/monitor/runner `1/0/1`,
  inner/outer/launcher `1/1/1`. Its journal records
  `REFUSED_WITHOUT_DELETION` and `removed: []`. It stopped on 195 process
  identities with 829 unreadable field entries; later dependency checks were
  not reached. The ordinary record-only consumer recorded
  `FAILED_INVESTIGATED`, all four recorded PIDs absent, no registry mutation,
  and unchanged old consumed output holds. This is not build-admission
  consumption or a relabelled old hold.
- Readback owner01: original command exit `1`, zero-byte `readback.json`, and
  exact stderr `sudo: A terminal is required to authenticate`. No privileged
  reader ran. Root's earlier successful `sudo -n -l` permission listing did
  not prove unattended authentication. The listing result is reported by the
  retained root review; no separate listing transcript was supplied here.
- Terminal owner02: source only, unrun when released. It requires the user's
  terminal before creating a fresh output directory and invokes the exact
  unchanged read-only command. The failed owner01 and original source seal
  remain intact. There is no cleanup adapter or retry execution in this packet.

## Exact retained evidence

[originals.tar.gz](originals.tar.gz) contains 81 regular members, 627,722 original
bytes. Archive SHA256:
`40f10b61670f0c8f249f49b60794d8e2a22f37abeee7262f5799c413d4f649b7`.
[The member manifest](archive-member-manifest.json) identifies every original
absolute locator and exact archived path, byte hash, mode, uid/gid, and nanosecond
mtime. PAX mtime uses the exact decimal nanosecond value. Every member was
independently reread without extraction and compared with its stopped original;
all 11 consumed-evidence references also matched. See
[custody-review.json](custody-review.json).

Archive groups:

| Group | Contents |
| --- | --- |
| `retirement-source/` | Original sealed source proposal, its manifest, static evidence, historical predecessor and full finite diff. |
| `failed-verify-owner/` | Materialized scripts, plan/preparation/seal, exact launcher/console/status, refusal, journal and failed-investigated consumption. |
| `failed-verify-run/` | Original watcher source, log, status, PID receipts and runner result; no fresh process scan. |
| `readback-source/` | Original sealed fixed read-only reader, exact five-file/two-parent scope, 195 refusal obligations, old helper and finite diff. |
| `authentication-owner01/` | All original command/hash/timestamp/status files, including the empty stdout and authentication error. |
| `root-review/` | Root source review and original #493 issue-comment response. |
| `terminal-source/` | Fresh owner02 terminal wrapper, complete wrapper diff, source-only static checks and seal. |

Original source seals remain embedded unchanged:

- Retirement source: `c50e35adabc168d099dc12b030eee7c570f853043d11f29c379a9c91eaed6586`.
- Readback source: `a777127dfcd052de9edf9a84ba0e9e42b924cbdccc62657f4502d1c42eeafe61`.
- Terminal continuation: `ada8efd8d76df51b8ad0d1177b2325de5be8671dc903c7910010e46d3817d930`.

## Concrete terminal continuation

The prepared command for the user to run in their own terminal is:

```sh
bash /tmp/pix-m7-stopped-media-root-readback-terminal-20261015/commands.sh
```

Wrapper SHA256:
`2143a3202a267cb3cc260eca30e9092096ed650b22877903e93e7714c1dea087`.
It rechecks the original sealed reader packet and captures the actual command
status under `/workspace/tmp/pix-m7-stopped-media-root-readback-20261015-02`.
It does not accept an alternate path or arbitrary command. Authentication stays
in the user's terminal; no password is sent to the agent or stored. It changes
no sudoers policy and installs no helper.

The sole privileged action is the unchanged fixed timeout plus isolated Python
reader. It only reads selected metadata and process references; it cannot
unlink, stop another process, alter source, or authorize removal. Outer timeout
124 remains distinct from inner status. Even a later complete zero result would
be a scoped snapshot, requiring root review and fresh ordinary dependency
checks before a separately authorized cleanup continuation. No exemption for
unreadable/new processes or consumed output holds is supplied here.

Custody work used source/receipt reads and compact archive verification only;
no process census, privilege command, device/runtime operation, media hash,
cleanup or original mutation was performed by this lane.
