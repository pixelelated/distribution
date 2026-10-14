# M7 offline component qualification — October 14

This standard no-NIC VM run is **complete and retired**. Qualification remains
partial: no new firmware, production pin, RC designation, device, provider account
or owner data was involved. The lifecycle completed both640×480 and1280×800
profiles before its90-minute deadline. [Original result consumption](consumption.json)
retains35 submitted owners, including their failures; [retirement](retirement.json)
records2,652,819,456 allocated bytes removed. No completed disks/media remain.

## Verified results

- **#575:** compiled French09afa replacement descriptions fit640×480 and1280×800;
  global and per-game walks return0, no game launch. Final1280 settings are byte
  identical. The earlier global640 walk normalizes incremental states0to2,
  deliberately equivalent under D-UI-083. A raw whole-file cmp failure is retained;
  subsequent parsed readback and source intent establish unchanged preferences.
- **#581:** three source-staged callers in small03 and four in small04 complete
  with preservation assertions. Small05 completes the remaining two French640
  refusals using display-only helper1a7714fd81. Their controlled runemu exits250,
  engine calls0, original ES/session/unshare/frontend restoration0, no remaining
  namespace tasks. The known card path breaks at its final slash and the filename
  remains intact. Updated English640 layout proof is still due. No native Dolphin
  gameplay, shipped package or retained-device upgrade claim.
- **#567:** four child-only tracer controls isolate the original ES SIGXFSZ:
  PulseAudio memfd ftruncate64MiB under8MiB FSIZE. Sealed81d618 gives only ES a
  finite64MiB ceiling plus a separate8MiB output tmpfs/export guard; nine guard
  controls pass. Its first corrected ES run fails the missing-log assertion.
  Exact source ignores --log-path and defaults to warning;84faea63d9 uses the
  supported private INI route and information logging, waiting for API idle and
  captured startup line within the original40seconds. Success, no-account,
  failed lookup and no-new-work API cases all pass. Native ES/listener0, no forced
  cleanup/remaining tasks, output guard pass. Success identifies one synthetic
  game and calls a **simulated ctl** once; no-account exits77 with no prepared
  stamp; failed lookup and no-new-work do not top up. UI confirmation branches
  and actual proxy integration remain distinct qualification.
- **#574:** full-library sanitizer attempt stops1 on the inherited MD5 unaligned
  load. Keep the original failure; a separate memcpy repair is source-only.
  Independent instrumented RVZ reader concurrency/lifetime and five byte-exact
  Dolphin padding comparisons pass0 with empty sanitizer stderr. Full format,
  independent DolphinTool/CHD, repaired MD5 and complete wrapper proofs remain due.
- **#582:** fresh-client and allowed existing-alias complete Steam callers pass.
  Corrected71e66 CRC fixture reproduces the defect: extraction1, subsequent
  retry0 despite absent executable and no new acquisition. Separate valid-client
  control passes with bytes/types/inodes/links and beta choice preserved.
  Synthetic transport/recording only; no actual Steam client ran.

## Original failures and observation limits

Earlier controls used a wrong ZIP local CRC offset; its original failure stays.
Two watcher submissions refused before payload due invocation/activity-dir errors.
Initial ES binary mode0644 failed126; corrected0755 proof is separate. Mount
hotplug needed bounded enumeration. The original serial wrapper broke a final
heredoc delimiter; corrected guest-command02 preserves its newline. None is
relabelled as successful runtime proof.

Dolphin entry timeouts before input remain failures. Reinspection of the original
French frames shows the selected game/header/footer: the earlier black/clock-only
assessment was wrong, not evidence of a rendering defect. A valid entry does not
turn a timed-out unlaunched case into a pass. The new two-case run supplies proof.

The first index output-guard pass did not contain native logs: the unsupported
flag sent them elsewhere. Its original parent census did not include /var/log,
so unchanged parent files does not prove those logs were untouched. The corrected
fixture captures the actual required native information lines through its bounded
mount. No original receipt is rewritten. FSIZE findings are not resident-memory
measurements or browser savings.

## Evidence layout

[Frame index](frame-index.json) binds individually reviewed PNGs and explicitly
labels rejected/incomplete cases. Dolphin PPMs were converted losslessly; conversion
receipts retain identities, while duplicate raw rasters were retired. Other host
captures are historical evidence, not accepted UI baselines.

`host/` keeps source controls, original serial/visual receipts and failure records;
`watchers/` keeps the original terminal results. `guest/` retains exported case
receipts; `guest-archives/` contains selected original logs/JSON from guest bundles.
[Archive disposition](archive-disposition.json) records every archived member's
size/hash and selection. Synthetic ROMs, caches, executables, private keys, raw
configuration snapshots and duplicate large quota-fill payloads are omitted.
No image or owner-library content is published. Public test fixtures remain
reproducible from their source commits. SHA256SUMS seals retained regular files.

## Next

#583 traces the proxy RVZ path before combined acceptance. Compile/test the
MD5 candidate314da58d6; build independent format tools under fresh admission;
finish updated English Dolphin layout and index UI/actual proxy proofs. Inspect
the public Steam archive offline before repairing partial-install retry. Then
compose the stable20261001 foundation, clean/retained install and final image
checks, independent audit and H700/SM8550 builds. No issue is closed here.
