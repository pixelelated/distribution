The exact reviewed source packet is preserved in source-originals.tar.gz. Extract fresh and verify its SHA256SUMS before use. The original tool build script is unchanged; source-only lifecycle revision02 fixes only staging/hash-binding close.py. No runtime or compilation is claimed.

# Native save tool build and CDI authoring — prepared, UNRUN

This is the minimal outer execution packet for the unchanged
`/tmp/m7-mkdcdisc-source-plan-20261014/build-tool.sh`, followed by the prepared
Tetris2 authoring command. It launches no test suite, game, emulator, VM,
container, package installer or firmware build. No packet program, compiler,
author or allocation ran while this source packet was prepared. The original
tool plan and its source bytes are unchanged.

The existing #584 numeric process/subreaper/pidfd pattern is reused by `work.py`;
`census.py` is byte-identical600f1a59. `owner.py` is a fixed two-stage host owner,
submitted through the existing `watch-build-submit`/`watch-build`/admission
mechanism. It uses the host's existing systemd user manager for actual kernel
resource limits. No general job framework or new host package is introduced.

## Availability and truthful limits

Parent-authorized read-only availability checks found the uid1000 manager socket
at `/run/user/1000/bus`, systemd259.5, default memory accounting enabled and
cpu/memory/pids controllers enabled through `user@1000.service`.
`host-availability.json` retains the query's original0/stdout/stderr. No scope
was created. The installed systemd259.5 resource-control/scope manuals confirm
MemoryMax, MemorySwapMax, CPUQuota, scope OOMPolicy and RuntimeMaxSec. The future
native owner uses a fresh exact unit name; an existing/unknown unit is refused.

| Bound | Actual mechanism |
| --- | --- |
| Native family4GiB memory | User scope `MemoryMax=4294967296`; actual `memory.max` must equal that value before compilation |
| No swap | `MemorySwapMax=0`; actual `memory.swap.max=0` checked |
| Whole-family OOM | Scope `OOMPolicy=kill`; actual `memory.oom.group=1` checked; any observed OOM fails |
| One CPU | Scope `CPUQuota=100%` (`cpu.max` quota=period) plus inherited affinity to one currently allowed CPU; unchanged Ninja `-j1` |
|128 tasks | `TasksMax=128`, with actual readback |
| Build600s; author120s | Separate original `Popen.wait`/monotonic deadlines and exact stage receipts; no timer reset/retry |
| Native family780s | Inner alarm;15s finalizer. Scope RuntimeMaxSec800 is an independent manager backstop; outer owner800s wait and30s cleanup |
| Compiler/object files256MiB each | Build child `RLIMIT_FSIZE`, inherited by compiler descendants |
| Authored disc/temp padding1GiB each | Author child `RLIMIT_FSIZE`; distinct from compiler and log limits |
| Named logs16MiB each | Owner checks each second and terminates its stage on excess; this is a monitored bound, not a filesystem quota |
| Private scratch2GiB logical bytes | Admission reserves it; owner scans only its private scratch/artifacts each second and fails on excess; this is a monitored bound, not a hard filesystem quota |

The4GiB limit is a kernel cgroup bound across the native build/author family,
not a per-process address-space claim. The watcher and outer receipt owner sit
outside it so they can preserve original OOM/termination outcomes. No
RLIMIT_AS fallback is silently selected if controls are unavailable at launch.
Original process returns are kept, including negative signal exits. A timeout
does not become a fabricated success or fabricated exit124.

The exact mkdcdisc source `disc_layout.hpp:30` selects333000 sectors for normal
74-minute padding; `disc_layout.cpp:71–76` estimates that padding and
`build_cd.cpp:66–79` creates it in the tool's temporary input tree. `main.cpp:422`
passes its private temp directory into `build_cd`. Thus a1GiB author-file ceiling
allows the roughly full-CD output and its separate padding file; a16MiB file
limit would be wrong. TMPDIR stays under the fresh private scratch. No padding
flag or game-code change is made to fit the fixture.

## Exact inputs and preservation

`inputs.json` binds the original build script, source tar, matching development
package, host compiler/runtime/tool identities and the57 selected Tetris2 files
(5,705,793 bytes including its BSD notice). The dev.deb was already fetched and
verified by root at21:08; its SHA is
`31b95aa3c65d384fbe73001eb697c3e5219dd4f46930fe6d1cf9281b75b0aaea`.
The source plan's earlier “not downloaded” text is historical; its preserved
`deb-readback.json` records the later data-only verification. No download or
install is part of this allocation.

Source archive SHA:
`92215196a70dd8e31e0641c1698c20978fbeab23eb70498dbad709c1848ef632`.
The unchanged build script checks that archive, the dev package, actual host
libisofs runtime and native Ninja, privately extracts/copies dependencies,
configures PNG disabled/downloads disabled, then builds only `mkdcdisc`.
Compiler flags/tool/source behavior are unchanged. It writes only its fresh
work directory; HOME/cache/TMPDIR are private. No shared SDK/cache writes.

The author uses byte-identical private copies of the existing game inputs:

```text
scratch/work/build/mkdcdisc
  -B scratch/game/1ST_READ.BIN
  -D scratch/game/tetris2-disc
  -p scratch/game/IP.BIN
  -o scratch/Tetris2-M7.cdi
```

`-B` is retained because the author's supplied executable is already scrambled.
The original input manifest and every selected source/game/host dependency are
checked before and after successful execution; private game copies are checked
after authoring too. Both actual tool ELF and authored CDI byte counts/SHA256
are recorded; no anticipated output hash is invented. Final artifacts move to
the owner's `artifacts/`, with tool and Tetris2 notices. The original source
archive, source/license pointers and libisofs package provenance remain bound.
This produces input for the separately prepared real native gameplay/VMU-save
fixture; it is not gameplay or save acceptance.

## Concrete allocation and commands

Run only after root releases the current exclusive firmware/runtime allocation.
The future owner is a normal uid1000 host process, never root. The host-tool
build is needed to create a licensed VM input; no physical device is involved.
All commands use the actual host namespace and authorized `/workspace` access.

```bash
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-01
TASK_PACKET=/tmp/m7-native-save-tool-lifecycle-20261014-02
TASK_OWNER=/workspace/tmp/pix-m7-mkdcdisc-20261014-01
python3 -I -S -B "$TASK_PACKET/prepare.py" --checkout "$TASK_TREE" --owner "$TASK_OWNER"
cd "$TASK_TREE"
tools/build-preflight
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
  --plan "$TASK_OWNER/retention-plan.json" --output "$TASK_OWNER/retention-report.json"
python3 -I tools/host-maintenance/build-admission prepare \
  --plan "$TASK_OWNER/admission-plan.json" --output "$TASK_OWNER/admission.json"
tools/watch-build-submit --owner "$TASK_OWNER/lifecycle-owner" -- \
  --activity-dir "$TASK_OWNER/logs" --admission "$TASK_OWNER/admission.json" -- \
  python3 -I -S -B "$TASK_OWNER/owner.py"
```

`owner.py` invokes the concrete existing user-manager capability as follows,
then verifies its actual resource files inside `work.py` before any compiler:

```text
systemd-run --user --scope --unit=OWNER_BASENAME.scope
  --property=MemoryMax=4294967296 --property=MemorySwapMax=0
  --property=CPUQuota=100% --property=TasksMax=128
  --property=OOMPolicy=kill --property=RuntimeMaxSec=800
  /usr/bin/python3 -I -S -B OWNER/work.py
```

Each native stage starts a separate owned process session. The numeric subreaper
census kills only identity-matched direct/adopted children on failure. Any forced
signal or unexpected descendant fails the stage. The outer owner can stop/kill
only its exact freshly created scope, then verifies its cgroup is empty or gone
and its original process has exited. A failed build never reaches authoring.
If resource observation fails, execution stops; it does not become an empty
census or an assumed cap. No automatic retries.

After all original watched channels close:

```bash
TASK_RUN="$TASK_TREE/.build-runs/ACTUAL_RETURNED_RUN_ID"
TASK_EXPORT=/workspace/tmp/pix-m7-mkdcdisc-evidence-20261014-01
python3 -I -S -B "$TASK_OWNER/close.py" \
  --owner "$TASK_OWNER" --run "$TASK_RUN" --output "$TASK_EXPORT"
```

Success retains actual build0 and author0, scope0, inner/outer PASS,
watcher0/runner0/launcher0, empty descendants/cgroup, unchanged original inputs,
actual tool/CDI hashes and original configure/build logs. Because the build
script is unchanged, its single original stage return plus `set -e` establishes
that configure and the selected Ninja target returned0; the packet does not
fabricate separate child-return receipts. Failure logs and real stage/scope
returns are retained instead of replayed.

The close command archives/re-hashes compact original records and checks actual
owner absence. It leaves tool/CDI artifacts and private build scratch intact.
Root reviews, records acceptance, consumes the specific admission through the
existing build-admission tool, then retires only `scratch/`; retain `artifacts/`
for the pending installed-image native save test. Neither acceptance, consumption,
retirement nor artifact publication happens automatically.

Additive revision02 stages `close.py` in the fresh owner and binds it in `config.json` and retention evidence. Both existing owner/work code-verification loops consume every config code entry. Original c8e23364 packet is unchanged; no runtime was executed for this correction.
