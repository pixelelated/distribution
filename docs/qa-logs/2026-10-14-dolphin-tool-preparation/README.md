# Independent Dolphin tool preparation — October14

Work for #574. The target binary and its static library bundle are now
accepted for VM testing. Actual loading and format conversion remain
unrun. The sections below preserve the original attempts and their results.

The source-only plan1c0e93 and runner eb70be990b were reviewed;48 finite host
controls passed. Compatibility source6797dd4853 passed52 controls, including
chunk-boundary SHA256 cases. These controls do not establish container behavior.

Can this be done on the VM? Target converter behavior belongs in the disposable
GENERIC_X64 guest. Preparing its target toolchain and proving host Docker/PID/
cgroup/admission cleanup uses the build host. No owner device or account data.

## Original attempts

| Owner | Original outcome | Diagnosis and retained limit |
| --- | --- | --- |
| attempt01 | FAIL1 | Pinned builder Python lacks hashlib.file_digest. No source-export child started. Narrow chunked-hash correction6797dd4853; no retry of this owner. |
| attempt02 | FAIL1 | Git archive applies upstream *.sln text eol=crlf, changing two committed blob sizes. Exact byte guard refused; do not waive it or count a partial export as source proof. |

Both exact containers were removed normally, watchdogs exited0, and original
launcher/runner/watcher/command host PIDs were absent. Admissions were consumed
as failed-investigated. The failed source scratch was retired:149,970,944
allocated bytes. Original failures are never rewritten as passing recovery.

Each attempt retains readable result/cleanup/acceptance/retirement files and a
lossless original-records.tar.gz. original-records.json binds every member's
original bytes. Git archive altered Source/dolphin-emu.sln36853→37348bytes and
docs/DSP/DSP_InterC/DSP_InterC.sln877→897bytes, exactly matching495/20LF-to-CRLF
expansions. Cached source was read-only throughout.

The next source exporter reads Git blob objects directly so attributes cannot
transform bytes or omit export-ignore paths. New export/configure need fresh
admissions. Source integrity, generated compile flags, compilation, ELF/loader
closure, independent formats and native proxy integration remain separate gates.

## Exact export and first actual configure

Sourcee6a97dd758 passes57 controls and attempt03-export:13,424 exact files,
173,273,422 tracked source bytes, original channels0, no OOM, normal container
removal and actual host exits. The export admission was consumed qualified.

Attempt03-configure remains FAIL1. CMake itself exited0 and source before/after
manifests match. Configuration-inventory exited1 because compiler normal
variables were incorrectly required in CMakeCache. Generated commands contain
the correct target compiler, but701 of806 commands lack requested release flags
because the retained toolchain overrides them. Pinned MbedTLS96 commands use
-O2; cpp-ipc9 commands explicitly append-O2. Preserve those source-backed
exceptions, require-O1/-DNDEBUG elsewhere, and verify actual generated commands.
The follow-up uses a private toolchain wrapper; retained inputs remain unchanged.
Original configure admission consumed failed-investigated, all cleanup PASS.
The~220MiB private source/configuration remains temporarily for the corrective
readback; no target converter has been compiled or executed.

## Correct flags, separate recovery and target compilation

Attempt04-export passes with sourceede19c15f9. CMake again exits0 and emits the
requested ordinary flags. Its inventory still returns1: the guard incorrectly
classifies the cpp-ipc C file as requiring the C++-only O2 override. Original
configure FAIL1, successful cleanup and consumed failure remain unchanged.

Runnerb65f782e20 passes88 controls. A separately admitted read-only recovery
verifies all75 original generated files (5,451,316 bytes), original source and
failed receipts. It passes701 ordinary O1/DNDEBUG commands,96 pinned MbedTLS O2
commands and9 pinned cpp-ipc C++ O2 commands. All recovery original channels0;
container/watchdog cleanup and actual host exits pass, admission consumed.

The single-job DolphinTool compile was submitted at06:17UTC to owner04's new
dolphin-build stage, admissiona1f27c627dc24d32b0870c3aa96dbbf0. Its existing
07:00:54UTC family deadline,4GiB memory/no swap,2CPU and6GiB sampled scratch
limit remain. This entry records the start, not completion. See the saved
session checkpoint for current status. No retained source/toolchain mutation.

## Compilation finished; original wrapper failure retained

At06:28:54UTC the original submission returned1. All831 compile/link steps
returned0 in703.295seconds, producing14,000,048-byte DolphinTool SHA256
f36a2c5f2f31e961ce605cc1c762f1e839f1880a0b1feeba4e09a1fccaa90d5b.
Container memory peak765,542,400bytes; no OOM or monitor error. Cleanup PASS,
watchdog0, host owners exited, admission consumed failed-investigated.

The final generated-file guard rejected two expected upstream byproducts:
Flatpak/org.DolphinEmu.dolphin-emu.metainfo.xml (empty→2605bytes) and
Source/Core/Common/scmrev.h (empty→261bytes). Root CMakeLists777–805 creates
empty placeholders then declares dolphin_scmrev BYPRODUCTS; ScmRevGen.cmake
populates both at build time. Other73 configured files are unchanged. Coordinator
readback also verifies all13,424 source bytes/modes and exact file inventory.
The original failure is retained under attempt04-build; no rebuild is planned.
The source lane prepares narrow output recovery and ELF closure before the
binary can be accepted for a VM invocation. No converter has executed.

Superseded owner03 source/configuration scratch is now retired223,055,872bytes;
all76 generated diagnostic/inventory files remain in a compact verified archive.
Owner04 is stopped but retained for immediate output qualification. No active
compiler/container/VM remains from this work.

## Accepted output and static ELF closure — next is actual VM use

Source0171115 passes77 focused controls. The separately admitted build-output
recovery passes all original channels0, full pristine source and exact generated
outputs; original build-wrapper1 remains. Its admission is consumed.

First closure remains FAIL1: readelf0 found PT_INTERP /lib64/ld-linux-x86-64.so.2,
but the SDK has the loader under sysroot/usr/lib. The image creates /lib64 as an
alias to /usr/lib; glibc installs there. No host library was substituted.

Narrow source4d15c80dce passes14 loader-mapping controls and the new
dolphin-closure-loader stage. All original child/container/watcher/launcher0,
cleanupPASS, watchdog0, host PIDs absent, successful admission consumed. Exact
byte-bound canonical loader and both observed interpreter paths agree.

Static closure covers19 ELF objects,38 version-provider checks,2,629 Sys resources
and original notices. The public QA bundle contains2,680 files/50,726,779 bytes;
manifest SHA25649b06305f103df552a9d6c7a145627a66b8cd5e240d34ddceb1df3592175ec0d.
It remains outside Git at owner04/stages/dolphin-closure-loader/vm20-bundle for
immediate VM staging. Compact raw readelf/owner records and bundle-manifest.json
are retained here; no compiler object or runtime binary is embedded in this
packet. No target or loader was executed. Actual installed loading, Sys lookup,
independent conversion/hash parity and native proxy tests remain.

Owner04 has no active process/container. All original stages are consumed and
must not be replayed. Its07:00:54UTC clock is not reusable or extendable; a new
VM allocation is independent and must bind the accepted bundle. Retain current
work/bundle only through immediate converter qualification, then retire scratch.
