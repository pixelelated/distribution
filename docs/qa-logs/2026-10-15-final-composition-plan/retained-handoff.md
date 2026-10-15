# Unchanged retained upgrade route — ready for root allocation

Independent of the native gameplay continuation. Source-only review; none of these commands has run here. Use the already qualified original source directly; it derives d4af/ES3178, the actual update tar and installed member identities from the completed final readback. No derivative, synthetic reseed, backup replay, UI matrix or frame-history gate is needed.

- Source: `/tmp/pix-m7-retained-loader-update-20261014`
- Full source seal: `bdeed5dd44a63e6e7ec7bb9e07109a77144318bc9143036879e9d9464bcfe6c9`
- prepare.py: `ffb489b06f605bfc8991b67f871ceeea7d9517c124fd4806d77cfc62ea4a1121`
- vm-lifecycle.py: `1bb740bd925e7f4838928888ee31304c80268afb675a9cbc87b380a4a5d76e46`
- guest.py: `22c34e33ff209e3364f4d8535d3ff2615da4fefa191e4c72d4bacd3c5f1cd580`
- New readback result SHA: `57575bcb84179c00e5e71ff341494b30f3103627d7bca2047588dc4dd4b5654d`
- New inputs SHA: `be406d291c670610471bb31c01379552f0b4e1bb6c5ff2d73c33f56d103a2bcc`
- Actual new update tar SHA: `b1457d7db7d7c93551ec56e2b2b913b78399eaa6c9b831761a514d87ec3f8666`, 2,123,141,120 bytes.

The protected retained02 disk exists at 8,631,549,952 bytes with its original OVMF. It carries the accepted real 20→d6a retained update and synthetic selected state, including accounts, settings, ROM/history and cloud activity. The base remains d6a; a prior fac608 proof used a disposable overlay and did not update this base. This continuation proves ordinary d6a→d4af update on a fresh writable overlay. It does not claim fac608→d4af execution. The existing preparer revalidates original phase/backup/consumed evidence and actual old owner absence; the admitted lifecycle checks whole backing hash/stat before and after. This source review observed paths and receipts only, not current actual-host quiescence or capacity.

```bash
TASK_SOURCE=/tmp/pix-m7-retained-loader-update-20261014
TASK_TREE=/workspace/repos/rocknix.worktrees/m7-p5-build-20261015-01
TASK_COORD=/workspace/repos/rocknix.worktrees/m7-player-setup
TASK_OWNER=/workspace/tmp/pix-m7-retained-loader-update-20261015-01
TASK_VERIFY=/workspace/tmp/pix-m7-image-readback-20261015-01/artifacts/result.json
# 136 is proposed; root checks current allocation, and lifecycle checks binding.
python3 -I -B "$TASK_SOURCE/prepare.py" \
  --checkout "$TASK_TREE" --verification "$TASK_VERIFY" \
  --retained-owner /workspace/tmp/pix-m7-retained20-20261014-02 \
  --retained-evidence /workspace/tmp/pix-m7-retained20-evidence-20261014-02 \
  --state-checker "$TASK_COORD/tools/pixelelated-state-check" \
  --state-checker-sha256 6d061af89caba886bd3417ee96dc01e37675655aa1ed92f423b9db02164dff03 \
  --owner "$TASK_OWNER" --vnc 136
cd "$TASK_TREE"
tools/watch-build --record-only -- python3 -I tools/host-maintenance/retention-report \
  --plan "$TASK_OWNER/retention-plan.json" --output "$TASK_OWNER/retention-report.json"
# Root reviews original report/watcher channels and capacity before admission.
python3 -I tools/host-maintenance/build-admission prepare \
  --plan "$TASK_OWNER/admission-plan.json" --output "$TASK_OWNER/admission.json"
tools/watch-build-submit --owner "$TASK_OWNER/lifecycle-owner" -- \
  --admission "$TASK_OWNER/admission.json" --activity-dir "$TASK_OWNER" --recursive-activity -- \
  python3 -I -B "$TASK_OWNER/vm-lifecycle.py"
# Supervise actual returned run and all original channels; then, after owners exit:
TASK_RUN=$(cat "$TASK_OWNER/run.path")
TASK_EXPORT=/workspace/tmp/pix-m7-retained-loader-update-evidence-20261015-01
python3 -I -B "$TASK_OWNER/close.py" \
  --owner "$TASK_OWNER" --run "$TASK_RUN" --output "$TASK_EXPORT"
# Root reviews compact originals, ordinary update and state/loader/base equality.
python3 -I tools/host-maintenance/build-admission consume --run "$TASK_RUN" \
  --evidence "$TASK_EXPORT/consumption-draft.json"
```

One 8 GiB/four-CPU/no-NIC guest. Work4200 s plus cleanup180 s, unchanged qualified ceilings. Ordinary stages: initial boot240 s; input format60/write180; update staging240; changed-boot readiness600; state reader100 each; loader15/15/30 with130-second serial/150-second host command; backing hash120 before/after; exact VM stop35. Input medium is tar bytes plus128 MiB rounded to MiB. Capacity forecast: 16 GiB private overlay, input medium,128 MiB records/UEFI margin. No reclamation credit.

Accept only original launcher/wrapper/command/monitor/runner/VM/guest/export success, changed boot ID and final BUILD_ID, exact selected bytes/modes and original retained receipts, strict three loader commands, default registry, no forced cleanup/survivors, and complete protected backing/OVMF equality. No public account value/hash is exported. Failure remains failed; do not retry or weaken an old-owner/refcount check. Do not retire or edit the retained base while this consumer exists. No handheld, radio, provider, abrupt-power, new restore UI or native-gameplay claim follows from this update proof.
