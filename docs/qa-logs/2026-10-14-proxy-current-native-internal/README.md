# #583/#584 current native proxy build — source only, UNRUN

This packet closes the **preparation** gap for a fresh `libraproxy_rchash.so`.
No build, container, service or VM was launched. No provenance PASS is claimed.
The older installed ELF remains `source_pins_verified:false`; its existing
native/service receipts are preserved. Only this directory is owned by this
internal fallback assignment. It is not a visible Herdr lane or a product change.

The next executable stage is `proxy-export`, followed only after original-result
consumption by `proxy-build`. Both use the existing admitted CHD/Dolphin runner.
`docker_owner.py` and `watchdog.py` are byte-identical; the source/export/build
selection is narrowly adapted. There is no bootstrap/configuration, new framework,
package dependency build, source download, image rebuild or target execution.
Historical `pix574.owner`/`pix574.stage` label names remain internal to these exact
copied owner helpers; the fresh container name is `pix583-native-<nonce>`.

## Exact inputs and source coupling

Coordinator identity: `b004cd4d0751bd871bfda11292b43280895f61ea`.
`plan/input-bindings.json` binds these current recipes and cached archives:

| Component | Pin | Archive SHA256 |
| --- | --- | --- |
| RAOfflineProxy, including glue and LZMA SDK | `c7ebd1b6e777f3751ff0ecdf8aba54045844e00d` | `88eef31acfa4104b20258bd5cea514ade30e6cdf35767ffc958009851d61898b` |
| rcheevos | `1433173220a7eaede6a9ed7a18e94117be1821e0` | `da635153d2dab228f3a3ef672bae56a7a6e5f57f1aacd420133521c5d3768cec` |
| libchdr, with its bundled codecs | `607694ca0812edfc9cc2030c64634fc2393668de` | `02e772a74c4e5ec110bb646e729e1910268d2dae2c76df2a1b35525cc3826a9c` |

All three archive hashes were read and verified here. They contain 857 regular
files / 13,241,497 bytes; the exporter retains all files, including licenses.
`plan/source-files.json` records every original hash/mode/size. The safe exporter
validates every header before extraction and refuses links, aliases, sparse or
special members and inventory changes. No native patch is selected. All 16 local
proxy patches touch only Python product/tests (`plan/patch-scope.json`).

The current RVZ padding fix is Python, from the accepted 112-file prepared tree
`/workspace/tmp/pix583-native-prepared-20261014-02`; its source receipt is bound.
No ES MD5 patch is applied to proxy rcheevos. The 53 current glue/LZMA files match
the frozen SDK source bytes read here (`sdk-native-comparison.json`), but that
comparison does not prove which sources produced the older installed ELF.
Fresh compilation reads the three current archives, never that SDK package tree.
#588's Python startup repair is separately owned and must be rebound to its own
source receipt before combined qualification; no race repair is included here.

`plan/make-target.sh` is byte-identical to the current recipe's entire
`make_target` function. It retains the exact source list, all five defines,
includes, bundled CHD/zstd/miniz/LZMA and archive handling. The wrapper supplies
GENERIC_X64 x86-64-v3, generic tuning, default O2/frame-pointer flags, PIC and BFD;
the recipe's final `-Os` is effective. `PKG_BUILD_FLAGS=+pic` does not opt into LTO.
The normal compiler wrapper uses `CCACHE_DISABLE=1` and private temporary files.
Original expanded compiler argv and diagnostics are retained, with no stripping.
This is a current-source target build, not a full package installation receipt.

## Resources and output contract

Physical SDK:
`/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement20`, mounted read-only
at its original `/workspace/repos/rocknix.worktrees/m7-pixelelated` prefix.
Exact compiler/linker/startup/runtime inputs plus the compiler/system header and
support inventory are bound. The large read-only header inventory is losslessly
compressed; its original uncompressed identity is retained. No cache symlink is
rewritten and no mutable cache is copied or hardlinked.

Builder: `ghcr.io/pixelelated/build@sha256:988c0ba586263caeba4be4c03bd16eee055c9d066657951e320087bb8226ee39`.
`--pull=never`, no network, read-only root, normal UID/GID, no capabilities,
no-new-privileges, 4 GiB memory/no swap, 2 CPUs, 256 PIDs, one GCC driver.
One **600-second family clock** covers export, review/admission and build; it
never resets or extends. **1 GiB sampled aggregate scratch ceiling**, not a disk
quota; 512 MiB host free-space floor and existing cgroup/OOM/CPU monitoring stay.
A timeout/resource fault or forced cleanup stays FAIL. New stage admission is
mandatory. No failed stage/family is replayed.

Successful build output:
`OWNER/work/proxy-native/sources/RAOfflineProxy-c7ebd1b6e777f3751ff0ecdf8aba54045844e00d/.x86_64-rocknix-linux-gnu/libraproxy_rchash.so`.
The build records hash/size, original GCC result, unchanged original sources,
ELF64 x86-64 shared type, four required `raproxy_*` exports, NEEDED/version tables,
and rejects RPATH/RUNPATH or a dynamic dependency other than `libc.so.6`.
This expected closure follows the older ELF inspection; an unexpected new closure
fails for review. No loader is invoked in the builder or on the host.

Each stage retains `result.json`, `container-result.json`, child JSON/stdout/stderr,
compiler identities, host/container resource samples, owned PID/CID cleanup,
watchdog result, and the original `watch-run.json` path. Consume original watcher
runner/command/monitor results plus submit launcher/tool-wrapper channels and
actual host process exits. `native-build.json` remains BUILT_UNQUALIFIED.

## Coordinator next command — UNRUN

Can this be done on the VM? **Yes**: loader/hash/service proof belongs on a fresh
no-NIC GENERIC_X64 guest. These two stages only compile the target in the existing
offline builder. Existing #583/#584 issue scope already records VM-first; the
coordinator records the concrete fresh allocation before execution.

After copying this sealed directory byte-exact into the coordinator checkout:

```sh
cd /workspace/repos/rocknix.worktrees/m7-player-setup
PIX583_REPO=$PWD
PIX583_PACKET=$PIX583_REPO/docs/qa-logs/2026-10-14-proxy-current-native-internal
PIX583_OWNER=/workspace/tmp/pix583-current-native-20261014-01
PIX583_STAGE=proxy-export
python3 -I -S -B "$PIX583_PACKET/plan.py" \
  --checkout "$PIX583_REPO" --owner "$PIX583_OWNER" --stage "$PIX583_STAGE"
PIX583_STAGE_ROOT=$PIX583_OWNER/stages/$PIX583_STAGE
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
  --plan "$PIX583_STAGE_ROOT/retention-plan.json" \
  --output "$PIX583_STAGE_ROOT/retention-report.json"
# Consume and review the original report result before the following admission.
python3 -I tools/host-maintenance/build-admission prepare \
  --plan "$PIX583_STAGE_ROOT/admission-plan.json" \
  --output "$PIX583_STAGE_ROOT/admission.json"
tools/watch-build-submit --owner "$PIX583_STAGE_ROOT/submit" -- \
  --admission "$PIX583_STAGE_ROOT/admission.json" \
  --activity-dir "$PIX583_STAGE_ROOT/logs" -- \
  python3 -I -S -B "$PIX583_PACKET/run-stage.py" \
  --checkout "$PIX583_REPO" --owner "$PIX583_OWNER" --stage "$PIX583_STAGE"
```

Consume `proxy-export` original results, then select `proxy-build` explicitly with
the same owner and repeat plan/report/admission/submit for that stage. Do not loop
both stages automatically. Original shared 600-second clock continues throughout.
Supervise actively; there is no off-session notification mechanism.

After successful build channels and actual host exits have been consumed:

```sh
python3 -I -S -B "$PIX583_PACKET/bind-provenance.py" --owner "$PIX583_OWNER"
```

This writes one fresh `OWNER/qualification-inputs/` with the exact ELF, compact
build receipt and `native-provenance.json`. The latter sets the **source linkage**
boolean only after checking original consumed success and rehashing source/ELF;
it explicitly labels VM runtime UNRUN. It does not upgrade old evidence.

## Exact serialized qualification handoff

1. Reuse the existing current-native integration/service owners and bounds in a
   **fresh** no-NIC VM20 allocation; no historical owner, port reservation, admission
   or completed service fixture is replayed. Root can combine the newly built ELF
   with #588's separately sealed Python startup case after inspecting the build.
2. Stage the newly exported ELF read-only, record its original `/usr/lib/`
   counterpart hash, and privately file-bind it at `/usr/lib/libraproxy_rchash.so`
   in this disposable guest. Verify `/proc/self/mountinfo` and bytes; a file bind
   is not reliably identified by `mountpoint -q`. Record the overlay explicitly.
   The accepted image archive stays unchanged. Restore/unmount in owned cleanup.
3. Inspect actual guest loader/`libc.so.6` identity and native NEEDED/version
   closure before loading. Preserve exact installed `libzstd.so.1.5.7` SHA
   `8526c748a90b34d9872159fdd311071ed1c391c879b41295848282fcace4e2f4` and
   `libcrypto.so.3` SHA
   `66d713b67c3d811ab73894b294ff40d7985a3273d26f493bdc9f59b79f2e2f77`.
   These are separate Python ctypes dependencies, not DT_NEEDED on the bridge.
   zstd is exercised by accepted RVZ input; crypto load/export resolution alone
   does not qualify Wii reconstruction. A changed dependency requires explicit
   fresh closure review; never copy arbitrary host libraries into the guest.
4. Existing `proxy-native-integration-source/fixtures/admit.py` already accepts
   a source-provenance receipt and hashes installed paths without loading. Stage
   `native-provenance.json` and `native-build-receipt.json` beside accepted inputs;
   `build_receipt` is a bounded relative path/hash/size row. Admission and driver
   must read the new overlaid ELF hash, not the historical `6c484a29...` identity.
   Retain the original admission and `/proc/self/maps` evidence. The existing
   native fixture's Python source binding is preserved unless #588 explicitly
   adds its independently qualified source; never relabel a changed fixture old.
5. Reuse accepted independent ISO/NONE-RVZ/Zstd-RVZ files and GameCube expected
   MD5 `118545082f24fc195a446d1ee7bbf816`, accepted small CHD closure and MD5
   artifacts; no converter rebuild or regeneration of accepted inputs is needed.
   CHD holder: `/workspace/tmp/pix574-chdman-closure-20261014-04/stages/chdman-closure/chdman-closure-01/vm20-bundle`.
   MD5 holder: `/workspace/tmp/pix574-md5-target-20261014/artifacts`.
   The prior 234-hash CHD receipt qualifies ES candidates, not this newly built
   proxy. Native proxy CHD parity/reset still needs its own current-ELF case.
6. Preserve original runtime result, resources, maps, child exits, unit lifecycle,
   bound synthetic signed queue and cleanup. Then consume admission and retire
   owned VM/media and private compiler source; retain compact logs/manifests and
   the small ELF only for the immediately queued integration. Current-source
   provenance alone does not close installed default-hybrid service, Dolphin
   gameplay/protocol interpretation, final composition, clean/retained image or
   #583/#584 combined acceptance. The accepted private-unified service proof
   remains scoped to that boot. #588 is separately owned; no duplicate fixture.

Read canonical next AGENTS/every-session rules, coordinator checkpoint, device-
builds, engineering-practices, instruction-files, working-principles, vm-first,
handheld-evidence and current #583/#584 criteria. Those were consulted here.
`tools/archaeology '583 native'` found no matching local rows; its GitHub search
failed network, while direct issue reads succeeded. This preparation makes no new
policy decision. Upstream contribution disposition remains in existing #583/#585;
this packet is fork QA plumbing, not an upstream fix or external submission.
Coordinator owns shared work-log/tracker integration; no shared record was edited.
