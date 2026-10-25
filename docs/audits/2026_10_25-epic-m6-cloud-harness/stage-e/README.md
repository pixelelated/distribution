# T13 stage E: the positives, kept on the branch (#660)

Every bug's case from stage E, as a command the acceptance re-run can repeat
from this branch. Each one fails on the unfixed tool and passes on the fixed
tool.

- **The unfixed tool** is `tools/` at **`8a2518fa44`**: a shared clone, `git clone --no-checkout --shared <this worktree> <U>; git -C <U> checkout 8a2518fa44 -- tools projects/ROCKNIX/packages/network/rclone/sources` (the rclone sources too: `cloud-test-backend shipped-default` reads `cloud_sync.conf.defaults` beside the tools, and a `tools/`-only clone reads an empty default -- found on the guest cycle).
- **The fixed tool** is this branch's `tools/` at `fixed-at` (`cee4bf481d` or later).
- **The drivers** take the tool's path first and `unfixed|fixed` second. They write only under `$TMPDIR`, print one verdict line last (`pos<bug>: unfixed-expectation-met | fixed-expectation-met | UNEXPECTED ...`), and exit 0 when that expectation is met.
- **The shell-run positives** use the isolation environment, with every backend brought down after its run.

Set up once, from the worktree's root:

```bash
export TMPDIR=/workspace/tmp/<yours>; mkdir -p "$TMPDIR"
S=docs/audits/2026_10_25-epic-m6-cloud-harness/stage-e
U=<the clone at 8a2518fa44>/tools      # unfixed
F=tools                                 # fixed
ISO="CLOUD_QA_STATE=$TMPDIR/state CLOUD_QA_NAME=rocknix-cloud-qa-m6t13 CLOUD_QA_S3_UPSTREAM_PORT=9092"
```

## Driver-based positives

| Bug | Driver | Unfixed: command, then the line it prints | Fixed: command, then the line it prints |
| --- | --- | --- | --- |
| #1066 (High) | `pos1066/drive.py` | `python3 -I -B $S/pos1066/drive.py $U/cloud-round-trip unfixed` -> `pos1066: unfixed-expectation-met (library deleted; control n/a (no content_root))` | `python3 -I -B $S/pos1066/drive.py $F/cloud-round-trip fixed` -> `pos1066: fixed-expectation-met (library kept; control REMOVED)` |
| #1060, harness half | `pos1060/drive.py` | `python3 -I -B $S/pos1060/drive.py $U/cloud-round-trip unfixed --backend $F/cloud-test-backend` -> `pos1060: unfixed-expectation-met (backend_files passes, backend_sizes passes, backend CalledProcessError)`. Without `--backend` it uses the unfixed backend beside the tool: `... backend returned)`, the same expectation met | `python3 -I -B $S/pos1060/drive.py $F/cloud-round-trip fixed` -> `pos1060: fixed-expectation-met (backend_files Fail, backend_sizes Fail, backend Fail)` |
| #1062 | `pos1062/drive.py` | `... $U/cloud-round-trip unfixed` -> `pos1062: unfixed-expectation-met (unassigned ['webdav']; absent file passes)` | `... $F/cloud-round-trip fixed` -> `pos1062: fixed-expectation-met (unassigned none; absent file fails)` |
| #1063 | `pos1063/drive.py` | `... unfixed` -> `pos1063: unfixed-expectation-met (clean fires, conflict fires)` | `... fixed` -> `pos1063: fixed-expectation-met (clean quiet, conflict fires)` |
| #1057 | `pos1057/drive.py` | `... unfixed` -> `pos1057: unfixed-expectation-met (2 vacuous PASS, 0 SKIP, control n/a)` | `... fixed` -> `pos1057: fixed-expectation-met (0 vacuous PASS, 2 SKIP, control FAIL alone)` |
| #1059 (with PL-15) | `pos1059/drive.py` | `... unfixed` -> `pos1059: unfixed-expectation-met (unknown cell named False (rc 2); setup went on True; counts on the line False; nothing-checked exit 0)` | `... fixed` -> `pos1059: fixed-expectation-met (unknown cell named True (rc 2); setup went on False; counts on the line True; nothing-checked exit 3)` |
| #1064 | `pos1064/drive.py` (needs a host with no `es_systems.cfg` at either path; it checks) | `... unfixed` -> `pos1064: unfixed-expectation-met (the empty probe passes step 25)` | `... fixed` -> `pos1064: fixed-expectation-met (the empty probe fails step 25)` |
| #1069 | `pos1069/drive.py` | `... unfixed` -> `pos1069: unfixed-expectation-met (tar -tzf rc 2)` | `... fixed` -> `pos1069: fixed-expectation-met (tar -tzf rc 0)` |
| #1070 | `pos1070/drive.py` | `... unfixed` -> `pos1070: unfixed-expectation-met (correct fails, hard-coded-3 passes)` | `... fixed` -> `pos1070: fixed-expectation-met (correct passes, hard-coded-3 fails)` |

The `...` stands for `python3 -I -B $S/pos<bug>/drive.py <tool>/cloud-round-trip`, the same form as the #1066 row.

## Shell-run positives

| Bug | Unfixed: command, then what it prints | Fixed: command, then what it prints |
| --- | --- | --- |
| #1058 | `env $ISO CLOUD_QA_PORT=9080 $U/cloud-test-backend up --backend sftp` -> `up: webdav serving <state>/data at http://127.0.0.1:9080 ...`, rc 0 (then `env $ISO CLOUD_QA_PORT=9080 $U/cloud-test-backend --backend webdav down`) | `env $ISO CLOUD_QA_PORT=9080 $F/cloud-test-backend up --backend sftp` -> `error: '--backend' after 'up': options go before the subcommand (...)`, rc 2, nothing listening |
| #1067 (High) | `env $ISO CLOUD_QA_PORT=9083 $U/cloud-test-backend --backend sftp up`; then `printf 'ls -1 /etc\n' \| sftp -q -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o BatchMode=yes -i $TMPDIR/state/sftp/qa-sftp-key -P 9083 <the stanza's user>@127.0.0.1 \| wc -l` -> the host's `/etc` entries (232 on the build host; count only), and the stanza's `user =` is the host login; then `--backend sftp down` | the same with `$F` -> `Can't ls: "/etc" not found`; the stanza user `rocknix-qa`; the host's keys refused (`ssh -o BatchMode=yes -p 9083 <host-login>@127.0.0.1 true` -> `Permission denied (password,publickey)`, rc 255); `ssh -i <QA key> -p 9083 rocknix-qa@127.0.0.1 id` -> `"id" not implemented`, rc 1; then `--backend sftp down` |
| #1068 | `$S/shim1068/build.sh $TMPDIR/shim1068`; `PATH=$TMPDIR/shim1068/obscure:$PATH env $ISO $U/cloud-test-backend --backend webdav rclone-conf` -> rc 0 with a `pass =` line carrying the clear QA value (smb and ftp the same); `PATH=$TMPDIR/shim1068/chmod:$PATH env CLOUD_QA_STATE=$TMPDIR/fresh $U/cloud-test-backend --backend s3 ls; stat -c %a $TMPDIR/fresh/s3-host.conf` -> 664 | the same with `$F` -> rc 1, `error: rclone obscure failed; no stanza written ...`, no `pass` line; the S3 config -> 600 |
| #1060, backend half | `env CLOUD_QA_STATE=$TMPDIR/no-such $U/cloud-test-backend --backend webdav ls` -> rc 0, no output | the same with `$F` -> `error: no endpoint state at <...>/data; 'up' first`, rc 1 (a missing prefix under a live state still lists empty, rc 0) |
| #1061 | `git show feature/m6-tooling-guards-657:.githooks/secret-patterns > $TMPDIR/p; ( SECRET_PATTERNS=''; . $TMPDIR/p; grep -a -c -E "$SECRET_PATTERNS" $U/cloud-connections-test )` -> 1 | the same on `$F/cloud-connections-test` -> 0; `$F/cloud-connections-test` -> `Ran 26 tests` / `OK` |
| #1065 | `printf 'x\n' > $TMPDIR/log; grep -c 'outside the saves folder' $TMPDIR/log 2>/dev/null \|\| echo 0` -> `0` then `0`, which CAP13's old `warned not in ("", "0")` passes | `grep -n "outside the saves folder\" in log_since" $F/cloud-round-trip` -> CAP13's presence test on this call's log; the sweep of the other `grep -c ... \|\| echo 0` lines is in 02 |
| #1081 | `grep -c cloud_device_id $U/cloud-census` -> 1 | `grep -c cloud_device_id $F/cloud-census` -> 0; `grep -n cloud_sync-device-id $F/cloud-census` -> the `cat ... \|\| echo unset` line |

## What only a guest shows

The guest halves of #1057, #1062, #1064, #1065, #1069 and #1070 run in the
one cycle on #660, and their lines go in `02` § The guest cycle.
