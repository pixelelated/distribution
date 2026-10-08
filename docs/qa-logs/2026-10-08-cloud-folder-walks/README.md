# Independent-folder standard walks — #527

The two corrected standard walks pass on installed replacement18 at 640×480
and 1280×800. All 16 frames were directly reviewed. The original wrong-screen
control remains rejected, including under the corrected comparison claims.
This qualifies QA navigation; the [full-suite/protocol disposition](../2026-10-08-pixelelated-replacement-18/qualification.md)
separately preserves the original failure and combines the unaffected results.

The immutable firmware is distribution `7f58b7b1c592908dcd0ba5987955e59aaa79fe66`,
ES `1d76b3da7da75794066df1c089931b890304da7a`, bundle
`f557176651026f59bb5931993b12491a6019c0383321fb89fa1a05a596514fe6`.
QA navigation/witness source is `2e484871bd`; reviewed comparison claims are
`7233b237ee2a8a05b090fb4276081648b26129b8`. Product paths are unchanged between
the image and QA trees. No product source overlay was used. Each packet binds
the installed hashes, original command/results and actual owner exit.

## Expected route and frames

The cloud hub's CHANGE CLOUD FOLDER opens the three independent path rows.
A opens the initially focused SAVES FOLDER editor. START submits its unchanged
value once; the editor closes without a provider probe or setting write.
The next B returns from CLOUD FOLDERS to the hub at CHANGE CLOUD FOLDER.
The standard witness reads the synthetic cloud for its own hash comparison;
that is distinct from the product's no-probe behavior.

| Point | 640×480 | 1280×800 |
| --- | --- | --- |
| Selected hub row | [Frame](corrected640/report/walks/confirm-cloud-folder/02-hub-change-folder-row.png) | [Frame](corrected1280/report/walks/confirm-cloud-folder/02-hub-change-folder-row.png) |
| Saves editor | [Frame](corrected640/report/walks/confirm-cloud-folder/03-folder-editor.png) | [Frame](corrected1280/report/walks/confirm-cloud-folder/03-folder-editor.png) |
| Unchanged value returns to selector | [Frame](corrected640/report/walks/confirm-cloud-folder/04-folder-result.png) | [Frame](corrected1280/report/walks/confirm-cloud-folder/04-folder-result.png) |
| Back returns to hub | [Frame](corrected640/report/walks/confirm-cloud-folder/05-after-dismiss.png) | [Frame](corrected1280/report/walks/confirm-cloud-folder/05-after-dismiss.png) |

[Small-panel index](corrected640/frame-review.json) and
[large-panel index](corrected1280/frame-review.json) include the initial hub
and the separate editor-only walk. Both before/after witnesses preserve exact
configuration/credential hashes and modes, validation-context paths, and local
and remote file hashes. These are synthetic fixtures, not a personal library.
Changed-path/refusal branches and EN/FR fit remain the qualified, unchanged
[CF05/PL-003 evidence](../2026-10-08-m7-audit-resolutions/PL-003/README.md);
this QA-only change does not claim to recapture those branches or locales.

## Discriminating comparison

[Original review](original-review.json) shows the old walk's “editor” was the
selector, its “result” was the carousel, and its last frame was the FBNeo game
list. The old walk produced frames with no command error but did not exercise
the intended confirmation. Preserve that distinction from a product failure.

[Initial comparison](corrected1280/initial-frame-diff.md) failed on 18 unclaimed
regions. Direct baseline/current review accounts for the added CHECK CLOUD
FOLDERS row and resulting scroll, editor title, selector behind the keyboard,
unchanged return, and Back returning to the hub instead of reopening a keyboard.
The isolated walk retains Game Boy fixtures that the earlier full-suite MATCH
operation removes; only the measured 31-pixel FBNeo neighbor edge is claimed,
following the documented #455 fixture effect. Neither baseline nor masks changed.
The [corrected comparison](corrected1280/corrected-frame-diff.md) passes all eight
screens with zero unclaimed regions; [old control](corrected1280/old-control-frame-diff.md)
still fails on six unclaimed regions using those same claims.

## Results and retention

Both original watched jobs have five zero result channels and actual owner
processes absent; see each `owner-consumption.json`. The 70-file small and
82-file large packets are hash sealed. Two earlier submissions stopped before
VM execution with rc2 (unsupported watcher flag, then missing activity directory);
their original records remain under `launch-failure01/` and `launch-failure02/`.

After acceptance, exact owned QEMU/provider shutdown and closed ports were
verified. [Retirement](retirement.json) removed all four private scratch owners,
including their key, guest disk and backend: 2,257,588,224 allocated bytes.
No personal device/cloud operation ran. The copied historical baseline subset
is eight visual PNG references, not a VM disk. The main regression has also
completed; its runtime is retired and its compact evidence is retained separately.
