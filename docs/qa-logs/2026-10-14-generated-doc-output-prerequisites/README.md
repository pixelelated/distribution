# Generated documentation fixture: source-time prerequisites

Additive source-only correction to packet `e71b57cc43460b07b1637508a46358d52bebbffb`
at `docs/qa-logs/2026-10-14-generated-doc-output-internal/` in the
`m7-browser-memory-570` checkout. The original packet, product proposal, and
failed owner's records remain immutable. No fixture, compiler, build, container,
VM, or service was run by this source lane. Root owns execution and acceptance.

The first control failed before documentation generation: sourcing the complete
function file expands `CONFIGXML="${PROJECT_DIR}/${PROJECT}/config.xml"` at
baseline line 216. `PROJECT_DIR` was unset under the unchanged `set -eu` body.
The original command/runner exits are 1; monitor exit is 0. The retained owner is
`/workspace/tmp/pix493-generated-doc-control-20261014-01`, and its watched run is
`/workspace/repos/rocknix.worktrees/m7-player-setup/.build-runs/20261014T185231Z-00f63ebf`.
The owner has exited and scratch was retired by root. `prerequisites.json` binds
its original console, launcher result, and runner result. Do not replay it.

## Narrow correction

The fixture now binds `PROJECT_DIR` to the real checkout's `projects` directory.
Full sourcing also executes the real XML query for `SUBDEVICES`. The host has no
`/usr/bin/xmlstarlet`; the retained replacement20 SDK provides the actual host
binary and its libexslt/libxslt/libxml2 dependencies. A new private `host-bin`
wrapper uses that binary with an SDK `LD_LIBRARY_PATH` scoped to its child only.
It does not alter the SDK, use its compiler, fake XML output, or install anything.
The wrapper is outside each temporary Git fixture and contains only an `exec`.

Before the seven existing controls, the fixture checks exact checkout input and
SDK hashes, then executes the real XML query for GENERIC_X64 and H700. Expected
selections are empty and `DDR4`/`DDR3`, respectively. Empty selection may return
0 or 1; nonempty selection must return 0. Unexpected output, stderr, loader
failure, or changed input is a failure. The result records both query results.
The actual full shell source still performs the same query on every case.

`BODY`, including `set -eu` and full `. "$1"`, is byte-identical to the original.
So are `candidate-functions`, `generated-doc-output.patch`, and `bindings.json`.
No functions are extracted, removed, replaced, or masked. The actual admission
tool is imported unchanged and now hash-bound before import. Its source-state
comparison and real tracked-mutation refusal remain mandatory. Original
baseline/candidate bindings and all seven documentation/environment controls
are unchanged; no product file is changed by this packet.

## All inputs of the exercised shell path

| Actual source/function | Inputs supplied or derived |
| --- | --- |
| Full-file source-time XML assignments | `PROJECT_DIR`, `PROJECT`, `DEVICE`, actual `projects/ROCKNIX/config.xml`, real `xmlstarlet`, `tr` |
| `clean_doc_cache` | `ROOT`, `DEVICE`; derives `DOCTMP` inside fresh private fixture |
| `start_system_doc` | `SYSDOCROOT`, `SYSDOC`, `ROOT`; watched candidate additionally requires marker, `BUILD`, `DEVICE` |
| Conditional templates | Both `templates/HEADER.md` and `templates/SUPPORTED_EMULATORS_AND_CORES.md` are absent in the bound checkout; absence is checked and preserved, with no invented template bytes |
| Body fixture rows | Creates `DOCTMP`, writes the same synthetic system/emulator rows |
| `mk_system_doc` | Derived `DOCTMP` and selected `SYSDOC`; uses actual `ls`, `awk`, `sort`, `uniq`, `cat`, `rm` |
| Other host helpers | Real `/usr/bin:/bin` Bash, Git, `mkdir`, `basename`; existing Python standard library; no package hook or build entrypoint |

All remaining definitions in the full shell file are parsed but not called;
their kernel, bootloader, ES-system and image variables are not exercised.
`add_system_doc`/`add_emu_doc` are also not called by this synthetic control.
The original environment exporter and Makefile forwarding contract are retained
and hash-bound. SDK ELF inspection shows libexslt, libxslt and libxml2 depend only
on each other plus host libc/libm, with the host ELF interpreter. These three SDK
libraries and the XML binary are sealed. Actual host loader compatibility is
for the prerequisite execution to prove; static inspection is not a load PASS.

## Static result and next execution

`static-result.json` records Python AST, shell syntax, and exact-byte parity.
The full diff whitespace check flags only the unchanged patch's blank context
line; exact patch bytes are preserved. No runtime PASS is claimed. This is a tiny host build-tool control; the original
#493 host/synthetic VM-first rationale remains applicable. It is neither emulator
nor final-image qualification. Root retains responsibility for original command,
monitor, runner, launcher, process-exit and output consumption.

Use a new owner, from the coordinator whose distribution function file still
matches the bound baseline. This command is prepared, not executed:

```bash
TASK_DOC_PACKET=/workspace/repos/rocknix.worktrees/m7-candidate-compose/docs/qa-logs/2026-10-14-generated-doc-output-prerequisites
TASK_DOC_OWNER=/workspace/tmp/pix493-generated-doc-control-20261014-02
mkdir -m 700 "$TASK_DOC_OWNER"
tools/watch-build-submit --owner "$TASK_DOC_OWNER" -- --record-only --activity-dir "$TASK_DOC_OWNER" -- python3 -I "$TASK_DOC_PACKET/fixture.py" --checkout /workspace/repos/rocknix.worktrees/m7-player-setup --scratch "$TASK_DOC_OWNER/fixture" --output "$TASK_DOC_OWNER/result.json"
```

Each existing subprocess limit remains 10 seconds, as do both new XML query
limits. No background process or new resource framework is introduced. Input
hash checks read about 2 MiB of retained XML-tool bytes; each Git fixture contains
only its small function/configuration/documentation inputs. Root supervises the
original watch-build lifecycle. If inputs no longer match, prepare another
explicit derivative instead of editing this sealed packet or expected hashes.

Runtime acceptance still requires all seven controls, equal generated bytes,
candidate watched output inside BUILD, unchanged tracked source, missing-BUILD
refusal, and refusal of a real tracked-source mutation. The full image build
remains the actual integration proof after the unchanged product patch lands.
