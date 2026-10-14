# #574 fresh no-NIC guest: independent Dolphin format oracle

Prepared source only, **UNRUN**. Parent source is `4d15c80dce0b91eb0adf40fd24f156c5e771238a`; coordinator checkpoint is `4960aaa`. This is a new guest admission, not another owner04 stage. Every owner04 stage is consumed and its clock expired. Nothing here invokes the old owner, Docker, a compiler, a mount, a service, an emulator, or a downloader.

Can this be done on the VM? Yes: loading the retained x86_64 converter and sanitized hash candidate, and converting self-created nonbootable data, need no physical device or account. Coordinator alone admits a fresh no-NIC VM20, creates its private mount, supervises serial delivery, consumes the original result, and retires the guest. The worker has performed no runtime proof.

## Exact public input

Mount the coordinator's newly assembled public input read-only at `/tmp/pix-input`. Under it require **exactly** this packet's tree; other independent packets may be siblings of `pix574-format`, never children. `input-bindings.json` maps every non-bundle input below to its exact retained host source, byte length, and SHA256. The bundle's own fixed manifest binds all 2680 payload files. No symlinks or extra files are accepted in this tree.

```text
/tmp/pix-input/pix574-format/
  packet/                         every file of this NEW committed packet
    guest-run.py
    guest-work.py
    guest_support.py
    controls.py
    input-bindings.json
    README.md
    static-validation.json
    SHA256SUMS
  stager/guest-stage.py            immutable 4d15 source; not modified/imported
  oracle/run-independent-format.py
  oracle/bounded.py
  oracle/source-bindings.json
  original/make-fixtures.py        legal PX5740 generator, unchanged
  original/upstream/rvz-go-license
  bundle/                         entire accepted vm20-bundle, including notices/Sys
    manifest.json
    dolphin-tool
    ld-linux-x86-64.so.2
    lib/...
    Sys/...
    notices/...
  hash/pix574-regression-hash      actual candidate ELF, not a wrapper
  hash/lib/libasan.so.8
  hash/lib/libubsan.so.1
  evidence/md5-compile-result.json
  evidence/md5-original-result.json
  evidence/md5-contract-candidate.json
```

Bundle host source:
`/workspace/tmp/pix574-dolphin-configure-20261014-04/stages/dolphin-closure-loader/vm20-bundle`.
Manifest SHA256: `49b06305f103df552a9d6c7a145627a66b8cd5e240d34ddceb1df3592175ec0d`.
Actual Dolphin ELF: `f36a2c5f2f31e961ce605cc1c762f1e839f1880a0b1feeba4e09a1fccaa90d5b`.
Actual sanitized candidate ELF: `5e00ed65dc6ae8031c54c4309d3f1876be4b380e438a15b8281104402e9375b2`, source `314da58d68820a79b26f99a5b6c12f9bb37054d5`.

Host assembly is a **future coordinator action**: copy the exact new packet; copy the bundle as an ordinary tree; for each `files` mapping copy the one named `host_source` to the relative destination, verifying length/hash. Do not rerun export/configure/build/closure or import any runner to assemble inputs. Preserve the original MD5 outer FAIL1 receipt as supplied; successful compiled artifacts have separate accepted recovery and guest evidence. No historical result is rewritten or reinterpreted as an original PASS.

## Admission and exact guest command

Prerequisites: fresh VM20 x86_64 Linux, `/sys/class/net` contains only `lo`, Python **3.11+** (immutable `bounded.py` uses `hashlib.file_digest`), procfs with subreaper support, writable `/tmp/pix-output`, and coordinator-created **empty executable tmpfs** at `/run/pix574-scratch`, mode0700, capacity at most2GiB and at least128MiB free. `/tmp` needs at least the50,726,779-byte stager copy plus32MiB. The new owner additionally caps aggregate scratch/stager/output apparent and allocated bytes at2GiB, sampled each second. Nothing is installed in outer `/usr`, `/storage`, or an actual player's home. The guest OS UID stays root; the fresh HOME, XDG directories, USER/LOGNAME and Dolphin `-u` directory contain only synthetic state.

After admission and input/mount readiness, the **one guest work command** is:

```sh
python3 -I -S -B /tmp/pix-input/pix574-format/packet/guest-run.py --run-id format01
```

`format01` must be unused; substitute one explicit fresh simple ID for another admission. Do not resume/reuse its directories. This command does not create the mount or start the VM. Capture its original serial command exit, stdout and stderr; do not accept a shell pipeline's last exit as the original. Coordinator's VM owner must enforce the same240-second guest work budget and consume/retire it even if serial disconnects or the driver is killed. No clock starts anew between cases. Driver reserves the last5seconds for process cleanup (235seconds work), and reports FAIL on an overrun; the oracle's original60-second conversions and15-second hashes are unchanged. There is no address-space or file-size rlimit that could invalidate ASan mappings or renderer fds.

Optional **separate admitted** synthetic parsing controls, not part of that240-second oracle run:

```sh
python3 -I -S -B /tmp/pix-input/pix574-format/packet/controls.py
```

Prepared22 assertions cover path traversal/NUL, nested-session ancestry, reused PID identity refusal, supported/unsupported/truncated ELF interpreter records and exact SHA256. They are UNRUN here. They do not qualify actual Linux signaling or cleanup. No additional guest case matrix is requested by this packet.

## Execution and evidence boundaries

1. Verify packet/input identities, then execute the unchanged `guest-stage.py`. Its own output is `/tmp/pix574-dolphin-format01` and sibling `.stage.json`. Retain that original copy/receipt. Recopy it into the executable private tmpfs and verify every payload byte/mode. Copy and verify the candidate ELF and both sanitizer runtimes into the same private scratch.
2. Parse actual ELF `PT_INTERP` without readelf execution. Record invocation path, resolved file, size, mode and hash for the installed Dolphin/hash loaders and private loader. Record `identical_bytes` without requiring equality: stripped image bytes can differ from retained SDK bytes. Run installed and private loaders' `--list` against the real converter, and retain their actual resolution stdout. Then execute real Dolphin `convert --help` directly and through the private loader; original exits must be0 with expected help and empty stderr. Direct execution is the actual kernel/installed-loader route subsequently used by the oracle. No hash-wrapper substitution is permitted.
3. Generate the legal synthetic input using its exact private libzstd. Execute the unchanged independent oracle with **actual ELF paths** and their fixed hashes. It inherits only the explicit synthetic environment, private `LD_LIBRARY_PATH`, `ASAN_OPTIONS=detect_leaks=1:halt_on_error=1:abort_on_error=1`, and `UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1`. The Python oracle also receives that environment; failure to load any part of this composition is an original failure, not permission to replace the interpreter or disable sanitizers.
4. Require5 full synthetic RVZ decodes,2 independent encodes,2 full ISO roundtrips and2 candidate GameCube hashes:11 original native commands,9 conversion rows. All child exits must be0, no timeout, actual executable hashes exact, and all native stderr empty. The generator's other malformed fixtures are not exercised here; do not claim that suite was rerun. Recheck the private Dolphin payload unchanged before PASS.

Outputs are exclusive `/tmp/pix-output/pix574-format-format01/`: owner/start identities, monotonic deadlines, per-second process/disk samples, worker stdout/stderr, stage/generator/loader/help/oracle command start and original completion receipts, both loader identity records and loading outputs, copied synthetic manifest, oracle's individual original command logs/exits, cleanup and final result. `oracle/dolphin-none.rvz` and `oracle/dolphin-zstd.rvz` remain there, with exact SHA256/length/expected GameCube MD5 and generator/ELF bindings in `native-proxy-input.json`. These are ready inputs for a later separately admitted native proxy test; native proxy is **UNRUN** by this packet.

The supervisor is a Linux child subreaper. It records PID/start-tick/session/group identities and follows descendants across the oracle's new sessions. On failure/deadline it signals only current owned groups whose membership/leader identity still matches, then exact owned PIDs, and reaps adopted originals. Partial stdout/stderr and any already-written oracle receipts remain. A command killed before its immutable oracle can write its completion JSON has an observed/adopted original wait status in `cleanup.json` where available, not a fabricated command result; this makes acceptance FAIL. If any descendant survives, cleanup FAIL remains explicit and the coordinator retires the VM. No command-name killing or deletion of evidence occurs.

Success requires driver original0, `result.json` PASS within240seconds, worker original0, `cleanup.json` PASS/no forced signals/no descendants, the11 original native command receipts, and unchanged source identities. Coordinator must consume original host/serial/guest channels. Scratch and stager copies remain for inspection and are reclaimed by coordinator VM retirement after evidence export; this fixture does not unmount or remove them.

## Source-backed Sys distinction and limitations

Pinned Dolphin `6094cfcf7b8fba733b3116fdf3414d51c1c0e4a4`: `FileUtil.cpp:722–784` obtains `/proc/self/exe` on Linux; `LINUX_LOCAL_DEV` derives `Sys/` from its parent directory. Accepted generated `CMakeCache.txt` contains `LINUX_LOCAL_DEV:BOOL=ON`; its exact hash and these source files are in `input-bindings.json.source_evidence`. Direct execution and explicit-loader execution can give different `/proc/self/exe` identities. Both private ELF files are deliberately siblings of `Sys`; this is a source-backed layout, **not a measured resource-lookup result**.

`ConvertCommand.cpp:115–120` parses options before `SetUserDirectory`/`UICommon::Init`; `OptionParser.cpp:373` prints help then exits. Therefore help proves loading/CLI only. Real conversions take the initialization path with the oracle's explicit new `-u`; they do not prove every resource was opened from this Sys directory. Every result records `sys_lookup_measured:false`. No resource lookup trace, game launch, full-disc integrity, Wii/CHD coverage, provider/account action or native-proxy acceptance is claimed.

Static validation only: AST parsing, exact source/input hash inspection, scoped diff/whitespace checks. No worker import, controls, target loading, compiler, VM or container was run. Guest prerequisites/loader compatibility and timing remain actual-runtime acceptance items; no source blocker was found in the retained inputs.
