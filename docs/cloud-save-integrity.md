# Scoped save integrity verification

Refs #517; D-CLOUD-181. This is a host QA/operations procedure, not a new
player flow or a replacement for CHECK CLOUD FOLDERS. M7 order remains
#515 -> #508 -> #507 -> assembled firmware/adoption/release qualification.

## What each check means

| Check | Evidence | Limit |
| --- | --- | --- |
| Folder readiness | Selected category listing/classification | Does not prove payload integrity |
| Byte integrity | Successful bounded reads, provider hashes and stable before/after identity | Does not establish historical progress or catch an already-damaged file with a matching hash |
| Container structure | PNG chunk CRC/zlib/scanline checks; RZIP v1 lengths/zlib; RASTATE v1 block boundaries | No image rendering, core deserialization or game-specific SRAM validation |
| Local/cloud equality | Exact relative-path comparison and hashes, with read errors/races reported separately | A difference does not establish a winner; timestamps alone do not choose progress |
| Playability | Separately scoped game/core loading evidence | Never implied by an offline structural pass |

Raw saves, sidecar metadata and unknown formats receive byte checks and an
explicit unsupported-structure result. Do not call repeated-byte SRAM corrupt
without a game-specific basis. PNG interlaced scanline layout is not checked.
Limits/unsupported versions require review, not an assumption of corruption.

## Collection contract

1. Name the selected save root and authorized read transport. A personal
   operational read is separate from release QA, which uses synthetic data.
   Never export credentials or invoke a backup/restore/migration writer to
   inspect data. Exclude ROM libraries and settings archives unless separately
   scoped; small-file categories are not necessarily small.
2. Obtain a complete successful metadata inventory and provider hashes.
   Record the collector's scope, flags, exit code and byte/file/time bounds.
   Reject duplicates, invalid paths, absent hashes and oversize inputs. A
   truncated/failed list is not an empty folder. No lossy text filter belongs
   on the authoritative JSON or binary stream. Restrict private files and
   produce a separate sanitized report; credentials are never collected.
3. Read each enumerated object into private numeric payload filenames,
   recording each exit code and byte count. Bound per-file and total work.
   Re-list the same selected root and compare identity, size, mtime and hash.
   Changes fail the packet rather than silently mixing versions. This is
   before/after observation, not a transactional provider snapshot.
4. Inspect exact local counterparts separately, preserving missing, unreadable,
   differing and changed-during-read outcomes. Check for extra local saves
   within the actual allowlist. Read current client pointers, automatic-sync
   settings and retained recovery state; remote rewind cannot reset these.
5. Run the offline verifier. Keep the per-file report private. Hash/structural
   evidence cannot prove the historically desired game progress. Preserve
   originals/recovery files; a validation result never authorizes replacement.
6. Record the outcome, controls and limits. Retire downloaded scratch after its
   named proof, retaining compact private manifests/reports. This scratch is
   not the independent recovery-copy project (#518).

Long reads use `tools/watch-job` with an actual PID, result and progress log.
The active agent consumes terminal results and reports completion. The monitor
writes local state; it does not itself deliver a chat notification.

## Offline verifier

`tools/cloud-save-integrity` uses Python's standard library and performs no
network or device operations. Its packet contains `before.json`, `after.json`
(full successful rclone `lsjson --files-only --hash-type Dropbox` results),
`ordered.json` (before sorted by Path), `reads.json` (ordered index/rc/bytes),
and `payloads/0000`, `0001`, etc. The collector is responsible for complete
scope and truthful receipt codes; the verifier cannot reconstruct missing
remote metadata or certify the collection transport.

```sh
tools/cloud-save-integrity /private/packet --report /private/new-report.json
tools/cloud-save-integrity-test --rclone /path/to/qualified/rclone
```

The report refuses overwriting. Exit 0 means scoped byte checks passed with no
supported-container error; playability remains unverified. Exit 1 records
per-file failures; exit 2 refuses an invalid packet/report. Bounds: 4096 files,
128 MiB total, 64 MiB/file and decompressed stream, 8 MiB/metadata input.
Collector limits may be smaller. Default output contains only aggregate
results. Reports contain hashes, so keep them private.

Dropbox hashing follows its [content-hash specification](https://docs.dropboxapi.com/dropbox-api/docs/technical-reference/content-hash),
with independent rclone controls at zero length and around 4 MiB boundaries.
RZIP v1 follows [libretro-common's reader](https://github.com/libretro/libretro-common/blob/master/streams/rzip_stream.c);
RASTATE follows [RetroArch's state writer](https://github.com/libretro/RetroArch/blob/bdba046fa6766380bc2457532f38e589df769aaf/tasks/task_save.c).
These validate envelopes, not the embedded core state.

## Carry-forward to existing work

- **#515 targeted repairs:** synthetic complete-manifest cases (including benign
  credential-like filename substrings), stale/failed reads, conflicting versions,
  cancellation, retention and verification cost. Reuse these checks where the
  repair actually needs byte proof; derive layouts from emulator writers.
- **#508 adoption:** assert local pointers, automatic-sync settings and obsolete
  migration consumers separately from cloud contents. Replacing firmware alone
  must not be mistaken for resetting stored configuration. No private owner
  compatibility branch is added.
- **#507 audit:** review those implemented contracts in the frozen product delta;
  this operational review is not the independent milestone code audit.
- **#518 redundancy:** later independent recovery design and synthetic restore
  drill; a current provider hash or provider rewind is not another backup copy.

No ES screen or IA changes occur here. Existing qualified CF01-CF15 source
proof remains attributed to its original source; CF10 assembled firmware
adoption remains pending. No new screenshot claim is made for this host tool.
