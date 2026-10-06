# Approved five-tree cleanup — #459

The maintainer approved the exact proposal: “Yes, you have my approval.”
D-INFRA-017 permits only replacement03/05/06/07/08, one at a time through
`tools/fork-worktree remove … --force`. No removal has started. No filesystem
reserve change is authorized. #456 preservation preparation is complete.

The fresh preflight finished at 03:12:13 UTC on October 6; all four result
channels are zero. Actual runner/watcher/command and both child processes
were absent at 03:12:20. Receipts and the sealed harness are in `preflight/`.

- Rehashed 15,206 retained files, 42,878,140,697 bytes; 27 git source inputs
  and submodules, all five branch heads and tracked diffs match custody.
- Traversed 4,221,608 directories across the four project storage roots;
  all 235 qcow2-suffixed files/backing chains passed, with no discovery or
  qemu errors, backing references into these trees, or container mount matches.
  Directory symlinks are not followed; this is the recorded scope, not a
  claim about arbitrary host files. The five internal disks are test fixtures.
- Full large preservation/dependency reports stay at their original local
  paths; their SHA256 values are recorded here. Preserved objects remain in
  the three stores documented by the earlier proposal. Keep runtime-01:
  accepted runtime-02 references its independently verified objects.

## Only remaining execution prerequisite

At 03:02:30, noninteractive sudo required interactive authentication. This
is not an automatic approval-review rejection or a request for deletion
approval again. The earlier 02:22:23 root report passed, but is too old to
serve as the immediate live-process check for new removals.

The maintainer has been asked to run this read-only watcher and leave it
running, then reply “running”:

```sh
sudo /usr/bin/python3 -I /tmp/pixelelated-approved-cleanup-20261006/watch-process-references.py > /tmp/pixelelated-approved-cleanup-20261006/root-watch.jsonl
```

It only reads process references and writes JSON to stdout. It performs no
deletion, permission change or command execution. Every five seconds it
checks cwd/exe/root/arguments/fds/maps for the five exact roots; it stops
when all five directories are absent or after one hour. Its sealed source
and hash are retained here. There is no permanent sudo grant.

No root-watch report exists at this checkpoint. All five removal owners are
prepared but unsubmitted. The entry point rechecks source/diff, preservation
metadata/manifests, protected paths, surviving disk chains, current container
mounts, absence of QEMU and a clean UID0 snapshot less than 15 seconds old
before invoking the ordinary-user worktree helper. It verifies directory
and registration absence, retained branch/head, protected paths and actual
free-space delta after each removal. Failure stops the chain.

Expected historical gross recovery is 539.33 GiB; after 14.49 GiB of retained
preservation data, estimated net benefit is 524.84 GiB. Neither number is a
measurement of reclaimed space. `capacity-before-removal.json` is a live
pre-removal capacity sample. Actual recovery must be measured after execution.

Protect replacement14/current, unbuilt13, retained12, qualified10, source09,
every candidate bundle, original ROCKNIX RC2 and backing chains, shared source
cache, the recovered rclone input and all three preservation stores. The
exact protected paths/inodes/heads are in `protected-before.json`.

Can this be done on the VM? No: this is host allocation and host dependency
inspection. No physical device, personal cloud or product changes are involved.
The remaining release order stays P3 dedicated account proofs/upstream
preparation, then P4 fixes audit, then H700 and separately gated P5 work.
