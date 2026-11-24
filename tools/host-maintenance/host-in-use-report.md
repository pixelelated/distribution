# Host in-use report producer

This #493 producer covers direct Linux host use of exact, enrolled generated
build files and private generated build trees. The fixed installed executable is
`/usr/local/libexec/pixelelated/host-in-use-report`. It accepts zero arguments
and reads only the administrator-owned fixed enrollment manifest at
`/etc/pixelelated/host-in-use.json`. One enrollment can name several exact
batches. Repeated reads within that enrollment need no administrator
interaction after the administrator provisions the narrow invocation rule.
Adding individually enrolled files or trees, replacing their enrolled
identities, or extending the enrollment requires an administrator update.
Changes within a standing tree require a fresh successful observation.

## Consumer protocol

The producer writes one JSON object to a pipe or terminal on stdout.

| Field | Meaning |
|---|---|
| `schema` | Integer `1` |
| `status` | Aggregate `clear`, `busy` or `incomplete` |
| `scan_complete` | Whether all required host process and namespace observations completed |
| `manifest_sha256` | SHA-256 of the exact enrollment bytes, or null before they could be read |
| `started_at_ns`, `finished_at_ns` | Unix wall-clock nanoseconds |
| `expires_at` | Enrollment expiry in Unix seconds, or null while enrollment is unverified |
| `reason` | Null or a fixed machine-readable global refusal code |
| `tasks_scanned`, `mount_views_scanned` | Counts, without process or namespace identities |
| `batches` | Per-selection results with `selection_sha256`, `files`, `status`, `reason` and `matches` |

Exit codes are 0 for aggregate clear, 1 for aggregate busy and 2 for
incomplete or rejected invocation. Incomplete takes precedence over busy.
A valid report can have a completed scan and an incomplete batch when one
enrolled batch has changed or is absent. In that case the status of an
unaffected batch remains independently usable. Bind the exact batch digest,
the trusted invocation, the complete scan, and a fresh timestamp for the
decision. Missing JSON, an incomplete scan, or mismatched credentials,
manifest, selection, timestamps or exit status hold the decision.

`matches` counts tasks with each kind of reference. Its keys are `argument`,
`descriptor`, `executable`, `mapping` and `bind_mount`. An incomplete batch has
`matches: null`. Several tasks can share a mapping, descriptor table or mount.
Reasons are fixed codes such as `manifest_stale`, `host_namespace`,
`host_procfs`, `selected_identity`, `fd_incomplete`, `maps_changed` and
`mount_projection`. Invalid invocation or a lost output stream can return 2
without JSON. The invoking tool must retain stdout and the actual exit code.
Treat plain saved JSON as evidence only when it is bound to the trusted capture.

## Private enrollment

Store this exact schema outside Git. Each list member is an independent
selection. This schematic example uses placeholders for all machine inputs.

```text
{
  "schema": 1,
  "enrolled_at": <Unix seconds>,
  "expires_at": <Unix seconds>,
  "host": {
    "boot_id": "<UUID from /proc/sys/kernel/random/boot_id>",
    "pid": <inode from /proc/1/ns/pid>,
    "mnt": <inode from /proc/1/ns/mnt>,
    "user": <inode from /proc/1/ns/user>,
    "independent_mount_sha256": []
  },
  "batches": [{
    "build_roots": ["/absolute/path/to/build.example"],
    "files": [{
      "path": "/absolute/path/to/build.example/build/pkg/file.o",
      "identity": {
        "device": <st_dev>, "inode": <st_ino>, "uid": <st_uid>,
        "size": <st_size>, "mode": <st_mode as a JSON integer>, "links": <st_nlink>,
        "mtime_ns": <st_mtime_ns>, "ctime_ns": <st_ctime_ns>,
        "allocated_bytes": <st_blocks multiplied by 512>
      },
      "aliases": []
    }]
  }]
}
```

Use literal absolute paths below the reviewed generated `build.*` directories
on local ext4. Collect identities by metadata reads with the normal owner's
selection procedure. Review the file class and exact identities before
enrollment. The producer will refuse a symlink in any component, a different
file identity, or an ambiguous/non-ext4 selected mount. An optional alias is
an exact expected absolute or relative spelling, such as a canonical builder
path in an argument. Aliases are string comparisons only. The producer never
opens one. There are at most 16 batches and 512 total file rows. A name occurs
once per batch. Identical selections are refused.

To form `selection_sha256`, sort one batch's `build_roots` and each file's
`aliases`, then sort its `files` by `path`. Take SHA-256 of precisely
`json.dumps(batch, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')`
before adding any output fields. Match the manifest digest separately against
the exact bytes reviewed for this enrollment. Enroll multiple finite batches
at once when successive runs are known. Removed or changed files make their
own batch incomplete. A new boot, namespace identity, window, or file identity
requires explicit re-enrollment. A query never updates the enrollment.

## Administrator boundary

Provisioning is an administrator action. Install the reviewed producer bytes
at the fixed executable path as root-owned mode `0755`. Its directories, the
absolute system interpreter, and the system Python import directories must
remain under administrator control. The shebang starts isolated Python and
disables site initialization and bytecode writes.
Install the private manifest as a root-owned, regular mode `0600` file under
root-owned, non-group/world-writable directories. Use an atomic replacement
when changing it. Keep the approved file/manifest digests with the enrollment
record. Run in the initial host PID, user and mount namespaces with
`CAP_SYS_PTRACE` and the full host procfs visible.

If the administrator chooses sudo for unattended reads, an example policy
entry is below. Replace the principal and host with the explicit authorized
reader and build host. The scope is this exact command as root with empty
arguments and the normal restricted sudo environment. The command accepts no
path, flags, request body or output filename. The example grants no shell,
interpreter, manifest update or broader credential. [sudoers command matching and tags](https://www.sudo.ws/docs/man/1.9.14/sudoers.man.pdf)

```sudoers
retention_reader build_host = (root) NOPASSWD: NOSETENV: /usr/local/libexec/pixelelated/host-in-use-report ""
```

Once that single command is enrolled, the reader requests a fresh observation
without a prompt. Capture stdout through a pipe and keep the actual sudo
exit code. The privileged process writes only to the inherited terminal
or pipe. The unprivileged consumer owns any receipt file. The inspector uses
no subprocess and opens no writable file.

```sh
/usr/bin/sudo -n -- /usr/local/libexec/pixelelated/host-in-use-report
```

## Coverage

The reader checks the host boot and namespace identities and rejects filtered
or overmounted process views. It verifies the selected files and enrollment
before and after inspection. It enumerates tasks within thread groups, reads
the descriptor table, executable, cwd, root, command line, mappings and
mountinfo for each live userspace task, and checks identities again. The
checks cover ext4 inode aliases, memory mappings and exact file bind mounts.
Process disappearance, new or changed tasks, unreadable fields, changed
descriptor sets, mappings or mount views, and bounded reads that cannot
complete result in `incomplete`. Zombies, dead tasks and kernel threads do
not contribute userspace observations. The wall deadline is 105 seconds.
No paths, raw process attributes, inodes, PIDs, arguments or mount records
appear in the report. [Linux procfs interfaces and filtering](https://docs.kernel.org/filesystems/proc.html)

Overlay, known stacked, FUSE and network projections can hide a backing
identity behind another inode. A live projected mount view with no explicit
binding yields `mount_projection`. An administrator may record a digest for
an exact live mount entry **only** after confirming that its backing storage
cannot contain or alias any enrolled file. The digest covers the ASCII decimal
mount namespace inode, one newline, and the raw mountinfo record without its
terminating newline. Keep the review outside Git. A changed mount entry has a
different digest. If the backing relationship cannot be proved, leave that
entry out. [OverlayFS inode semantics](https://docs.kernel.org/filesystems/overlayfs.html)

This is a non-atomic snapshot for #493's separate retention decision.
Keep the existing owner, admission, incoming-link and stopped-container
checks. Registry holds, future-use declarations, backing relationships and
references held outside these userspace proc interfaces require their own
evidence. Use the report while the selected scope is quiescent and refresh
it before a separate authorized decision. The producer does not inspect build
payloads or calculate reclaimable disk space.

## Focused controls

```sh
/usr/bin/python3 -IBS tools/host-maintenance/test-host-in-use-report
```

The controls use temporary generated files and a fabricated proc tree. They
exercise repeatable clear reports, busy aliases/mappings/file binds, expired
or replaced enrollment and selected operands, independent later batches,
namespace and projected-mount refusals, process and FD churn, malformed and
changed mappings, redaction and the exit/stream interface. The fixture logic
can run on a VM. A VM cannot establish visibility into the build host's
procfs or the identity of its enrolled files.

## Tree consumer interface for build-tree-retention

The fixed producer entrypoint is unchanged. A v1 enrollment may add `trees`, a
bounded list of exact administrator-enrolled generated directories. Each tree is
`{"path":"/absolute/private/checkout/build.example","identity":{"device":1,"inode":2,"uid":1000,"mode":16832}}`
with the actual root identity. This is one standing enrollment per directory
identity and window, independent of the number of descendant files. File batches
and trees may coexist within the existing 16-result limit. A file-only manifest
and its wire response retain v1 compatibility.

For PC/P7, the tree key is the SHA-256 of sorted-key, compact ASCII JSON
`{"policy":"generated-build-tree-v1","path":<exact absolute root>,"identity":<four fields above>}`,
using the same encoding as `build-tree-retention:tree_key`. The producer emits
the usual v1 batch with that selection digest, `files:1`, and the five existing
match counters. The raw report additionally contains
`"tree_scope":"generated-build-tree-v1"` and `"tree_selections":[<tree keys>]`.
A tree key in that list is a scope marker. The existing captured result,
per-batch status, enrolled manifest digest and freshness checks determine use.

### Standing tree enrollment and limits

Use `"batches":[]` for a tree-only enrollment. Enroll either a literal
`build.*` directory or an exact package subtree below
`build.*/build/`, such as `/private/checkout/build.example/build/example-1/obj`.
For a nested enrollment the enrolled path and four identity fields belong to
the nested root, and only that subtree is reported. The retirement consumer
still verifies that the parent is an admitted build output. Select either a
parent or its nested subtree in a manifest to keep the scopes disjoint.
The root is non-symlink, with the enrolled nonroot UID and no group/world write
bit. All roots must be on the selected host ext4 mount and free of nested
mounts. This same enrollment covers new descendants
and later builds reusing the exact root inode. A new root or replacement root
requires enrollment once, including when adopting legacy output. An enrollment
does not adopt output ownership, authorize retention, or establish a consumer
hold.

The reader takes a no-follow descriptor-relative metadata snapshot of every
descendant, including directories and literal symlink leaves. Descendant
payloads stay unread. Special files, crossing a filesystem, missing members,
hardlink counts reaching outside the enrolled tree, and any detected identity
change hold the selection. Repeated hardlinks within the exact tree are indexed
by device and inode. Each pass permits at most 200,000 entries and 64 MiB of
relative-name bytes across the tree selections, at directory depth at most
64. There are two passes under the existing 105-second overall wall deadline.
A larger or unreadable tree holds.

Tree matches include descendant and root spelling and inode, file descriptors,
executable, cwd and chroot root, mapped inodes, directly recognizable argv
spelling and lexical relative operands, and same-filesystem binds of a
descendant, the tree, or an ancestor. Cwd and chroot root contribute the
`descriptor` count. The initial view and live task mount views are examined.
A foreign mount namespace exposing the tree at the same spelling is still
in use. Raw `nsfs` `net:[ID]` and `mnt:[ID]` records retain their identity.
A mount namespace pinned by a mount record or observed descriptor must have
an inspected view or be the enrolled initial mount namespace. Changed tasks,
FD sets or targets, argv, task links, maps, mountinfo or tree metadata yield a
hold. An initial-view bind can contribute one match even if the task counts
do not already represent it. Result fields stay redacted.

Projected views for trees require a separate
`host.independent_tree_mount_sha256` list, using the same namespace/raw-record
digest encoding as the file list. Omit it or use an empty list by default.
An approval is administrator-held backing evidence for **all** standing tree
roots and their potential descendants, grounded in the live attached backing
identities and applicable namespace. A file-only proof or a path/device guess
does not qualify. The reader checks the exact supplied digest and its current
record. It does not establish overlay backing independence from mount option
strings or query a runtime socket. Trees also require proof for unknown
filesystem types and explicit loop-mounted sources. Shared unqualified views
hold both scope types in a mixed scan.

### Administrator deployment and remaining Serval gate

The reviewed executable and the fixed manifest described above are the only
required installation inputs. With separately selected administrator authority,
place the producer at the existing fixed location and provision a root-owned
atomic manifest using the actual initial host boot and namespace IDs, the
approved window and the exact tree identities. The same zero-argument
command and ordinary consumer already read the resulting tree batch. No shell
or general runtime interface is part of that rule.

Serval's retained protected result for the different 15-disk scope and the
ordinary 22-overlay observation supplied no trusted backing evidence for these
trees. No tree-mount approval is supplied by this change. To qualify a real
current legacy or new scope there, the storage and runtime owners must verify
the live attached layer identities and aliases for every applicable view, or
the obstructing projections must retire normally before a fresh reader run.
The privileged executable and manifest have not been deployed by these tests.

The reader does not inspect queued or in-flight admission, legacy appliance
fingerprints, stopped-container declarations, arbitrary application intent, or
open references held outside the inspected userspace proc interfaces. Keep
the existing registry and ownership lock contract, both legacy-route holds
where applicable, retained evidence, and input/symlink checks. The report is
a point observation under that cut, never unlink authority.

The focused suite exercises the actual producer serialization and exit status,
the real `retention-report` parser/consumer, and
`build-tree-retention:clear_tree`, with only the fixed invocation and host OS
boundaries replaced by isolated fixtures. It verifies clear, busy and
incomplete outcomes without installing a helper or modifying host policy.
