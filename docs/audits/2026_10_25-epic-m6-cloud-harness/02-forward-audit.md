# T13 forward audit: the cloud test harness (#660)

Phase 2 over #660's checklist, the nine tools at `8ebaf8daad`'s bytes. Stage A
wrote § The runs; § Coverage, § Assertion shapes, § Positives and § Proofs
follow at stage B, and § The guest cycle in the window granted on #660.

## The runs

All on the build host, 2026-10-25 05:00-05:01 UTC, in the worktree, with
`TMPDIR=/workspace/tmp/m6-t13/tmp`. Raw outputs are under `.qa-scratch/t13/`
(gitignored). Wall times are `date +%s.%N` differences around each command.
The host's rclone is `rclone v1.60.1-DEV`.

### The four bare tests, the documented positive, the retired tool

| Run | Command | Exit | Wall | What it printed | A FAIL would mean ... | proved: |
| --- | --- | ---: | ---: | --- | --- | --- |
| `cloud-connections-test` | `tools/cloud-connections-test` | 0 | 1.9 s | `Ran 26 tests in 1.864s` / `OK` (26 `... ok` lines) | the connection module's staged transactions, its rclone-state handling or its shutdown cleanup diverged from a case, as judged by the module itself and the **host's** rclone (not the image's) | tool-run |
| `cloud-input-test` | `tools/cloud-input-test` | 0 | 1.0 s | `Ran 9 tests in 0.964s` / `OK` (9 `... ok` lines) | `wifictl` under `bwrap` with shimmed `nmcli`/`iwctl` (host bash, host coreutils) or `cloud_oauth` under the host's `node` broke one of its cases | tool-run |
| `cloud-capture-stamp-test` | `tools/cloud-capture-stamp-test` | 0 | 0.1 s | 14 `PASS` lines, `PASSED` | `cloud_capture`'s `finish()`, lifted by `sed` and run under the **host's** bash with `date` faked, no longer keeps one line per mode | tool-run |
| its documented positive | `git show f451252587:.../cloud_capture > $TMPDIR/old-cloud_capture; tools/cloud-capture-stamp-test $TMPDIR/old-cloud_capture` | **1** | 0.1 s | 6 `PASS`, 8 `FAIL`, `8 CHECK(S) FAILED` (first: `the old exit line is gone: last-capture: 1 line(s)`) | -- this is the FAIL: the pre-fix `finish()` overwrites the stamp with one line, and the test sees it | tool-run |
| `cloud-save-integrity-test` | `tools/cloud-save-integrity-test --rclone "$(command -v rclone)"` | 0 | 0.1 s | 24 checks (`PASS total=24`; 25 lines start `PASS`, the last being the total): 19 rejection and structure cases, 5 `Dropbox oracle` sizes (0, 4194303, 4194304, 4194305, 8388625) | the verifier accepted a corrupt, truncated, unsafe or changed packet, or its Dropbox content hash disagreed with rclone's (the one second implementation among the nine) | tool-run |
| `cloud-pair-migration` | `tools/cloud-pair-migration /nonexistent/a.img.gz /nonexistent/b.img.gz /nonexistent/c.tar` | **2** | 0.00 s | `This migration suite is retired. Use a historical source checkout for historical firmware; #508 qualifies manual cloud setup.` | -- it cannot FAIL on this tree: it refuses before anything (lines 58-63), keyed on `cloud_migrate_layout`'s absence | tool-run |

**The brief's counting line counts nothing here.** § 5 counts
`grep -c -E '^(PASS|ok)'`. The two unittest tools print `... ok` at the line's
end and `OK` alone, and the stamp test indents its `PASS`, so that grep reads
0, 0 and 1 for runs whose real counts are 26, 9 and 14. The counts above are
`grep -c -E ' \.\.\. ok$'` and `grep -c -E '^\s+PASS'`.

### The backends: up, ls, cat of a missing object, down

**Isolation, by the tool's own parameters:** `CLOUD_QA_STATE=/workspace/tmp/m6-t13/state`,
`CLOUD_QA_PORT` 9080 / 9083 / 9082, `CLOUD_QA_NAME=rocknix-cloud-qa-m6t13`,
`CLOUD_QA_S3_UPSTREAM_PORT=9092`. The reason is that `down` kills every
listener on its port (lines 565-591) and the M7 lane runs guests on this host.
Before the runs nothing listened on 9010-9099 and no QA container existed.
Each backend got one object by `put` first, so that `ls` and `cat`'s
present case have something to read.

| Backend | `up` | `ls` | `cat` of the put object | `cat no/such/object` | `reset` | `down` | `status` after | A FAIL would mean ... | proved: |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WebDAV `:9080` (`rclone serve webdav`) | rc 0, 0.0 s | rc 0, `6 t13/probe.txt` | rc 0, 6 bytes | **rc 1**: `cat: <state>/data/no/such/object: No such file or directory` | rc 0 | rc 0, 0.1 s, `down` | `not running`, rc 1 | the endpoint did not start, could not list, reported a missing object as present (blindspot 22/31), or left its listener up | tool-run |
| SFTP `:9083` (unprivileged sshd) | rc 0, 0.1 s; `note: this sshd cannot chroot unprivileged, so the remotes are absolute` | rc 0, `6 t13/probe.txt` | rc 0, 6 bytes | **rc 1**: `cat: <state>/sftp/data/no/such/object: No such file or directory` | rc 0 | rc 0, 0.1 s | `not running`, rc 1 | the same | tool-run |
| S3 `:9082` (MinIO container) | rc 0, 1.6 s | rc 0, `6 t13/probe.txt` | rc 0, 6 bytes | **rc 1**: `cat: no such file at the endpoint: no/such/object` (the existence check of lines 650-653; bare `rclone cat` of a missing key exits 0 on MinIO) | rc 0 | rc 0, 0.3 s | `not running`, rc 1 | the same; on S3 specifically, that the existence check stopped standing between `cat` and MinIO's exit-0 on a missing key | tool-run |

**Nothing left running** (05:01 UTC): `ss -ltn` shows 0 listeners on
9010-9099; `docker ps -a` shows 0 containers named `rocknix-cloud-qa*`;
`pgrep -f` for `rclone serve webdav`, `sshd -f /workspace/tmp/m6-t13` and
`minio server` finds no process other than the checking shell.

**For Q4, the images `up` would use, as resolved on 2026-10-25** (local,
nothing pulled; `docker image inspect`):

- `quay.io/minio/minio:latest` is `sha256:14cea493d9a3...`, created
  2025-09-07, label `version=RELEASE.2025-09-07T16-13-09Z`.
- `dperson/samba:latest` is `sha256:66088b78a198...`, created 2020-07-03.
- pyftpdlib is not resolved: FTP was not brought up at stage A.

**The argument order (a lead for stage B).** The option loop (lines 57-63)
stops at the first non-option, so a `--backend` after the subcommand is
ignored and the tool answers for the default (WebDAV) with rc 0.

```
tools/cloud-test-backend port --backend sftp    -> 9010 rc=0   (WebDAV's)
tools/cloud-test-backend --backend sftp port    -> 9013 rc=0
tools/cloud-test-backend caps --backend s3      -> hash=none modtime=no commit=partial bucket=no   (WebDAV's)
tools/cloud-test-backend --backend s3 caps      -> hash=md5 modtime=yes commit=atomic bucket=yes
```

The brief's § 5 loop writes `up --backend "$b"`; run as written, it would
have brought up WebDAV three times and called that WebDAV, SFTP and S3.

### The harness without a device

| Run | Command | Exit | Wall | Result | A FAIL would mean ... | proved: |
| --- | --- | ---: | ---: | --- | --- | --- |
| `--list` | `tools/cloud-round-trip --list` | 0 | 0.1 s | 55 lines, **45 cells**: two-device 11 (PAIR's 10 with `RETENTION`, plus `CONTRACT`), single-device 1 (A15), CAP 14, LINK 7, KILL 12 | the registries failed to load or print without a device | tool-run |

The brief's `grep -c -E '^(A|CAP|LINK|KILL)[0-9]'` reads 0, because every
cell line is indented two spaces; the count is `grep -c -E '^  [A-Z]'`.

### Four descriptions of one suite

| Where | Says | proved: |
| --- | --- | --- |
| `tools/vm-qa:36` | `round-trip  tools/cloud-round-trip  -- 27 steps over SSH against the QA cloud` | tree |
| `tools/cloud-round-trip` (AST) | 32 `step()` in `run_steps`, 2 in `prepare_device`, 46 in the file; 460 `check()` calls | tree |
| `docs/vm-qa-log.md:175` (2026-10-06) | `WebDAV/SFTP/MinIO-S3 round trips each106 PASS/0FAIL/0SKIP;318 total` | history |
| `docs/work-logs/2026_10-work_logs/2026_10_08-work_log.md:111` | `Both ordinary VM round trips already passed 108` | history |

A FAIL here would mean the four agree, and they do not. Which one a PASS line
certifies is stage B's question (Q7), answered from the tool's own summary
line in the guest cycle.
