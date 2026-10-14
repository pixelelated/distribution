# Installed UI outer lifecycle — source only, UNRUN

This supplies the missing outer owner for the already sealed narrow UI smoke.
It does not change that packet or repeat its accepted full source/frame controls.
Original packet: coordinator `docs/qa-logs/2026-10-14-installed-ui-smoke/source-originals.tar.gz`,
SHA256 `f720474af56d0532d1d898d74c87b8bd5aaac75c83c4aac93f197661de225b6e`;
inner manifest `c46457c66881e965ba4d5c078a9082aa341fba4dac7679c60665de391e9b1b35`.
The archive is extracted fresh, every original member and its manifest verified,
and original case scripts remain byte-for-byte unchanged.

Can this be done on the VM? Yes: one fresh installed GENERIC_X64 guest performs
the existing final-image loader/browser/phone/Wi-Fi/Recent continuation. Root
records its existing #571/#577/#578 allocation before launch. This is not another
build gate, provider qualification, radio proof or full UI matrix.

`prepare.py` consumes the **completed** image verifier's `result.json` beside its
original `inputs.json` and `candidate.img`. The result must bind distribution
`d6a87f05c1935516115b2cca1af22151a0209224`, ES
`3178b832b8d134198b2b4eede4f725d4ed283f8c`, and all existing UI member entries.
The original input record identifies the compressed image path/size/SHA256;
the verified raw image supplies its measured size. Preparation retains these
small original receipts. Full compressed-image hashing and bounded inflation
occur under the admitted owner. No second SYSTEM extraction is needed. The
clean result is produced on this actual fresh boot, not supplied as a manual flag.

The executable sequence reuses accepted `2026-10-13-library-vm/records/vm-lifecycle.py`
and only the QA-key portion of its `provision.py`, plus the original
`2026-10-13-clean-state-565/run-first-boot.sh`, canonical frozen networked VM helper,
`vm-serial`, `vm-stop`, watch-build-submit and admission tools. It:

1. Hashes the exact image, sparsely inflates it, converts to an independent
   QCOW2 and grows it to the existing 16 GiB minimum.
2. Boots once at 640×480, four CPUs and 8 GiB RAM, default boot files/kernel
   options, normal user NAT and one loopback-only SSH forward. It binds actual
   generated QEMU argv/PID/start ticks and checks the assigned ports first.
3. Runs the original untouched clean-first-boot helper **before** SSH key,
   access marker, synthetic settings, media or library provisioning. It retains
   the original serial report and verifies current-boot readiness and identity.
4. Creates one private disposable QA SSH key, writes its public key and the
   normal sshd service marker through serial, and starts the installed SSH unit.
   The installed host public key comes back through serial and becomes this
   owner's known_hosts entry. SSH multiplexing is disabled. No ES, catalog,
   cloud_oauth, browser, scanner/library or proxy overlay is introduced.
5. Calls the original smoke preparer, then original `run.py` once. Before any
   seams that packet performs the installed loader readback. Its only allowed
   binds remain synthetic rclone transport and wifictl enumeration. It performs
   original config byte/type/mode restoration and installed byte/mode readback.
6. Retains a compact postcheck of installed members, same boot, restored config
   receipt, absent seam mounts/browser/synthetic listeners, then stops the exact
   owned VM using the existing pidfile+disk helper.

Existing smoke bounds remain 60/210/90/90/210 seconds per stage and 900 seconds
for the whole smoke. The outer lifecycle reserves 1800 seconds including image
conversion, initial serial readiness (240 seconds), original clean proof
(180-second guest transport), provisioning and export; an independent 90-second
cleanup alarm follows. This scheduling allowance is not a new acceptance test.
Host commands preserve actual `wait()` status and separate timeout/error fields.
The owner enables and reads back child-subreaper mode before launching any
child. Detached case, SSH and Playwright descendants are therefore adopted even
between samples. The unchanged qualified `census.py` helper uses numeric proc
identity and pidfds, with no numeric kill or process-name pattern. Bounded
cleanup reaps original adopted-child statuses, preserves each active Popen wait,
and recenses after each parent exits. QEMU is excluded
from child cleanup and owned separately by vm-stop. Any forced host cleanup
prevents success. The private case output guard remains 128 MiB/1024 files;
the outer records/private browser temporary ceiling is 256 MiB/4096 files,
with 8 MiB per command stream. Host memory/PSI and QEMU RSS are recorded every
five seconds during command waits. The canonical 8 GiB guest bound is retained;
no host or per-service cgroup cap is claimed. No new backend/provider is started.

On an ordinary case failure, the original smoke's finally retains its restoration
results. A timeout or lost SSH may prevent restoration; the outer result stays
failed, preserves original partial records, and closes the actual guest and
host descendants. VM destruction is not labeled successful product restoration.
Raw original guest config archives and host private SSH/browser profile data
remain private scratch, never included in the compact export.

Exact commands, after root allocates the stopped-build host namespace and ports:

```bash
TASK_SOURCE=/tmp/pix-m7-installed-ui-lifecycle-20261014-revision02
TASK_COORD=/workspace/repos/rocknix.worktrees/m7-player-setup
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-p5-build-20261014-01
TASK_VERIFY=/workspace/tmp/pix-m7-image-readback-20261014-01/artifacts
TASK_OWNER=/workspace/tmp/pix-m7-installed-ui-20261014-01

# VERIFY names the completed verifier's actual artifacts directory; do not
# invent a receipt or reuse a partially failed owner. Ports below are proposals
# checked again immediately before launch; root allocates them with this owner.
python3 -I -B "$TASK_SOURCE/prepare.py" \
  --checkout "$TASK_TREE" --verification "$TASK_VERIFY/result.json" \
  --archive "$TASK_COORD/docs/qa-logs/2026-10-14-installed-ui-smoke/source-originals.tar.gz" \
  --owner "$TASK_OWNER" --ssh-port 10618 --vnc 118

cd "$TASK_TREE"
tools/host-maintenance/retention-report --plan "$TASK_OWNER/retention-plan.json" \
  --output "$TASK_OWNER/retention-report.json"
tools/host-maintenance/build-admission prepare --plan "$TASK_OWNER/admission-plan.json" \
  --output "$TASK_OWNER/admission.json"
tools/watch-build-submit --owner "$TASK_OWNER/lifecycle-owner" -- \
  --admission "$TASK_OWNER/admission.json" --activity-dir "$TASK_OWNER" --recursive-activity -- \
  python3 -I -B "$TASK_OWNER/vm-lifecycle.py"
```

The one outer watch admission already covers the smoke subprocess; no second
watch-submit or VM allocation is needed. Supervise the actual returned run,
`lifecycle-owner/console.log`, `records/resources.jsonl`, `smoke/result.json` and
eventual `vm-result.json`. Do not run close until original launcher/runner/owner
results exist and their processes have exited. This new allocation can follow
clean/retained work, but it uses its own fresh empty guest because the narrow
Recent fixture refuses a preexisting GB library. No retained library is erased.

```bash
TASK_RUN=$(cat "$TASK_OWNER/run.path")
TASK_EXPORT=/workspace/tmp/pix-m7-installed-ui-export-20261014-01
python3 -I -B "$TASK_OWNER/close.py" \
  --owner "$TASK_OWNER" --run "$TASK_RUN" --output "$TASK_EXPORT"
# Review original clean, smoke case/status/restoration/frame records and actual
# owner closure. This command is not part of close.py and never runs implicitly.
tools/host-maintenance/build-admission consume --run "$TASK_RUN" \
  --evidence "$TASK_EXPORT/consumption-draft.json"
```

`close.py` checks actual recorded owner/VM/descendant exit, retains all original
channels (including a failure or mismatch), and losslessly verifies its compact
archive. It does not consume admission, delete scratch, publish or claim acceptance.
A failure draft still needs root's investigation; monitor failure/mismatched
channels are explicitly retained and the existing consumption guard will refuse.
After root reviews/consumes, retire only this owner's QCOW2/OVMF/private key and
browser TMPDIR with the existing owner-scoped retirement procedure; never the
protected firmware, completed verifier artifacts or build tree. No commands
above were executed during preparation.

Revision02 preserves the old sealed draft unchanged at `/tmp/pix-m7-installed-ui-lifecycle-20261014` (manifest SHA256 `7527f36d896c090448268d3c4730ae36edfb3a7ac960473759b10ddfb5854c5d`). Only the serial physical-line correction, qualified subreaper/pidfd owner cleanup and corresponding copied-code binding/documentation change. The original smoke packet is unchanged. `serial()` rejects both newline and carriage-return input and emits one physical shell line. `census.py` is byte-for-byte the qualified retained-update helper; its source identity is recorded in `original-inputs.json`. No new runtime or test was executed.
