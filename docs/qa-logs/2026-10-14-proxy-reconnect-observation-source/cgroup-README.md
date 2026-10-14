# Actual proxy service: explicit disposable v2 boot — source only, UNRUN

Use a **fresh disposable VM20 boot with
`systemd.unified_cgroup_hierarchy=1`**, retaining the full-v2 prerequisite and
verifying actual kernel memory/PID limits. Do not adapt this image to v1 memory
limits, substitute an AS limit for a cgroup limit, or merely change the cgroup
path to `/sys/fs/cgroup/unified`. No product or installed-image default changes
are proposed. This packet qualifies a deliberately changed QA boot configuration;
it cannot establish service resource enforcement on VM20's default hybrid boot.

The original packet 57a138de95d0824617ebb5bd7b2476928d773650 and failed attempt 01
remain immutable. Selected receipts plus the **complete 1280-byte original fixture
archive** (SHA256 cdfa6fef8d1ed980d17318ea906944b474bd4d8e7fb81855d8b37e0f35853a51)
are under `cgroup-evidence/`. Driver/owner exited 1 before any command or proxy
startup, `commands=[]`, no driver cleanup error or remaining child. The external
cleanup receipt remains 0. No native accepted proof is replayed.

## Evidence and compatibility boundary

`compatibility.json` hashes the original failure and all five new guest records
from Steam attempt 11: mountinfo, self-cgroup, directory layout, systemd version
and kernel command line. They show systemd 255.8, compiled default **hybrid**,
a cgroup2 mount at `/sys/fs/cgroup/unified`, `name=systemd` at
`/sys/fs/cgroup/systemd`, pids and other controllers on v1, and no v1 memory
mount. No explicit cgroup boot option was present. A missing mount alone does
not prove absent kernel memory support.

The retained VM20 image tree's `configs.ko` contains the **compiled Linux 7.1.2
configuration**, read as bounded embedded IKCFG data without loading the module.
It says `CONFIG_MEMCG=y`, `# CONFIG_MEMCG_V1 is not set`, and
`CONFIG_CGROUP_PIDS=y`. The complete decoded configuration and module hash are
retained. This distinguishes it from the repository's older configuration header
and from its newer systemd recipe pin. The retained systemd executable/shared
library have 255.8/hybrid build strings. Their exact bytes, systemctl and configs.ko
are bound in this packet; the new guest must match these bytes and kernel release
before the service starts. This is a retained-image platform binding, not proof
of current source pins or qualification of new native builds.

The cached **official systemd-stable v255.8 archive**, SHA256
`e770b9c4b5e36c1badf94444a27c9cd427931251009e4363f3239ad45ff75f3d`,
was read without extraction/execution. Hash-bound excerpts establish:

- `src/shared/cgroup-setup.c:82`: an explicit unified-hierarchy argument selects
  full v2 unless an already mounted hierarchy has established another choice.
- `src/shared/mount-setup.c:104`: full v2 mounts directly at `/sys/fs/cgroup`.
- `src/core/cgroup.c:1851`: MemoryMax writes `memory.max` in unified mode; the
  legacy path writes `memory.limit_in_bytes`. A property readback by itself is
  therefore insufficient on this hybrid image with no v1 memory controller.

Primary source: [systemd v255.8](https://github.com/systemd/systemd-stable/tree/v255.8).
The [kernel cgroup v2 contract](https://docs.kernel.org/admin-guide/cgroup-v2.html)
describes controller availability, single-hierarchy membership, `memory.max`
and `pids.max`. Kernel documentation was checked online; versioned systemd HTTP
reads failed, so exact cached official source bytes supplied that part of the
research. No claim rests on a newer systemd manual's compatibility assumptions.

One boot argument is sufficient as the prospective choice; no dynamic controller
migration, cgroup remount, v1 fallback, `cgroup_no_v1=all`, or service limit removal
is added. The next boot must prove its actual resulting layout. If an earlier
mount, missing controller or changed image prevents it, admission fails.

## Source change

The packaged service/controller, prepared proxy hashes, seeds, bootstrap observer,
reference fixture, census, owner, lifecycle commands, worker timings, queue/award
assertions and original exits remain unchanged. `source_pins_verified` remains
false. The old explanation is retained as `prior-README.md`; this document
supersedes only its boot/cgroup admission and proposed owner command.

The additive `cgroup_guard.py` reads kernel files only; it never writes cgroups,
changes limits, signals a process, or starts a service. It requires one full-v2
mount rooted at `/`, the explicit boot option, memory+pids controllers, sole v2
PID1 membership, exact unit path and PID/start identity, actual finite limits,
and zero OOM/PID-limit events. Unreadable, aliased, missing or changed state fails.

`run.py` retains its old v2 check, records platform/layout facts, and checks the
owner's actual 1 GiB / 128-task group. The proposed owner command adds `TasksMax=128`;
this tightens its previously implicit task allowance. The service remains
512 MiB / 64 tasks. A fixture-only `ExecStartPre` performs the kernel checks before
actual proxy main; each ready incarnation repeats them and retains the result.
The original recursive cgroup census also rechecks the mount layout, so missing
visibility cannot masquerade as an empty group. Each pre-start check writes its
own original receipt, including failure; a failed check must not be bypassed.
The source unit's actual ExecStart/ExecStartPost and restart policy are untouched.

All existing timing/resource bounds remain: 240 s driver work + 30 s cleanup,
272 s owner child wait,280 s systemd owner lifetime + 20 s stop,310 s outer command
plus 10 s forced cleanup; driver 768 MiB AS / 120 CPU seconds / 4 MiB files; proxy 512 MiB AS,
120 CPU seconds / 4 MiB files; dedicated 64 MiB tmpfs with 48 MiB free,8 MiB staged inputs.
Neither deliberate idle SIGKILL nor a guard failure becomes a successful exit.
No guard or fixture was imported/executed by this worker.

## Exact next coordinator experiment — UNRUN

Allocate a **new owner and private VM disk**, with the same accepted compressed
image hash 1a23cf5740dbb69cdca76d753a0f6121c35e6e12f27649e792aeebc71e8cc490,
no NIC, and the existing lifecycle's finite deadline. The old owner stays failed
and retired. Plan the boot-setting seam before dispatch: the existing helper
has no kernel-argument passthrough. It boots the image through Syslinux; recorded
kernel command lines and `scripts/mkimage` agree. `boot/syslinux.before.cfg` is
also bound to the exact text found in a bounded read-only 16 MiB image prefix.

The smallest available provisioning seam is the fresh guest's **own private**
`/flash/syslinux.cfg`, before starting any fixture owner or proxy. Coordinator
stages this packet at `/run/pix583-service-packet` and retains the text/receipt on
its durable output media before the one planned reboot. The text adapter writes
only a new proposed file and refuses anything except the exact baseline bytes:

```sh
python3 -I -S -B /run/pix583-service-packet/prepare-boot-text.py \
  --input /flash/syslinux.cfg \
  --output /tmp/pix-output/proxy-cgroup-syslinux.cfg
```

Coordinator then applies that exact file to the newly owned guest's
`/flash/syslinux.cfg`, records before/after bytes and hashes, syncs/remounts the
private flash read-only, and performs the **one planned reboot**. This is not an
automatic retry of the failed fixture. All work remains inside the new lifecycle
clock; if its existing deadline cannot cover provisioning/reboot/proof/export,
stop for a separately admitted plan rather than extending/resetting it. No
live shared mount or accepted image is changed. No helper installs packages or
edits a boot disk automatically. The exact application/reboot belongs to the
coordinator's VM lifecycle seam, not a new worker runtime allocation.

After reboot, preserve `/proc/cmdline`, `/proc/self/mountinfo`, `/proc/1/cgroup`,
root `cgroup.controllers`, boot ID and systemd version; re-stage this sealed packet
and the already prepared source at the original paths. `run.py` independently
refuses if the actual mount/controllers/bytes/boot option differ. Provision the
same 64 MiB scratch tmpfs. Then the single service command is:

```sh
systemd-run --wait --unit=pix583-service-proof-owner \
  --property=RuntimeMaxSec=280s --property=TimeoutStopSec=20s \
  --property=KillMode=control-group --property=MemoryMax=1G \
  --property=TasksMax=128 \
  /usr/bin/python3 -I -S -B /run/pix583-service-packet/owner.py \
  --output /run/pix583-service-owner/run02
```

Consume all original channels/cleanup and unchanged lifecycle/award assertions,
plus platform/layout, owner kernel limits, every `cgroup-start-*.json` and
per-incarnation kernel limits. The expected deliberate idle signal 9 remains
recorded. Actual full-v2 boot, controller enforcement and service behavior are
still **UNRUN**. No replay of accepted native/format proofs is requested.

Prepared refusal criteria: hybrid/missing boot flag; missing memory/pids;
wrong/unlimited memory or PID cap; PID/group identity mismatch; unreadable or
aliased hierarchy; nonzero OOM/PID-limit events. These are source-enforced,
not runtime-tested. No additional runtime test matrix is allocated here.
