# Selected-root contract corrections after broad run02

The completed broad run02 reported 11 failures, zero skips. Seven were A0 expectations for retired discovery/flat-library behavior or a fault injected into the obsolete `lsf` command. Two A14 assertions still required deriving content paths from saves. Two A40 assertions expected provider-root fallback and flat-library restore.

The current-source branch now verifies only the selected structured library, explicitly selecting a different library/root before recognizing it, independent default selection, and real selected-path listing failures. The fault shim records every matched injection; the unreadable check requires a recorded `lsjson` fault, nonzero status, `STATE=unreadable`, no `STATE=empty`, and unchanged config. The selected ROMs and content-root failure cases also require a fault witness, no success stamp, and no restored ROM. Successful structured restore remains a positive control. The historical source branch retains its original discovery, coupling, and flat-layout expectations.

The focused extraction uses the actual candidate image BusyBox and rclone, records their identity, and preserves their SHA-256 hashes in fixture inventories. Current source `6f89bc7cecee5972909828103689e2c7c0711c30`: **14 PASS, rc 0**. Historical ref `3268015c`: **18 PASS, rc 0**. No fixture was silently marked inapplicable. Product sources did not change. `bash -n` and `git diff --check` passed.

`harness.patch` is the exact incremental change from the completed run02 harness. `summary.json` identifies the final frozen harness bytes. Root owns launching the next full watched suite; these focused results do not replace it.
