"""Record resolutions only after all final, independent acceptance receipts exist."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

root=Path.cwd();a=root/'docs/audits/2026_10_06-milestone-m7-p4-fixes-383'
q=root/'docs/qa-logs/2026-10-07-pixelelated-replacement-16'
read=lambda p:json.loads(p.read_text())
names=['qa20-acceptance','cloud02-acceptance','selected-content01-acceptance','content-routing01-acceptance','recovery-640x480-acceptance','recovery-1280x800-acceptance','supplemental02-acceptance']
for name in names:assert read(q/name/'acceptance.json')['result']=='PASS',name
assert read(q/'qa20-acceptance/acceptance.json')['identity_direct_frames']==15
assert read(q/'cloud02-acceptance/acceptance.json')['total_assertions']==318
assert read(q/'content-routing01-acceptance/acceptance.json')['direct_frames']==30
assert read(q/'phase7-source-readback/commands.json')['result']=='PASS'
stamp=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
proofs={str((q/name/'acceptance.json').relative_to(root)):hashlib.sha256((q/name/'acceptance.json').read_bytes()).hexdigest() for name in names}
(q/'phase7-source-readback/final-acceptance-receipts.json').write_text(json.dumps(dict(verified_utc=stamp,result='PASS',receipts=proofs,scope='Final acceptance composition; earlier failed runs retain their original results.'),indent=2)+'\n')

text=f'''
## Final candidate16 qualification — {stamp}

Distribution `ee014909137e03706e0b3020b8396be589aaa705`, ES
`72494bc72e3d64d4dcfeb4e6478052bbdf166c5b`, immutable bundle
`7f98f2d22985d11fe9c150015457894caf460104c9ce44abd16074167f23815a`.
The new [source readback](../../qa-logs/2026-10-07-pixelelated-replacement-16/phase7-source-readback/commands.json)
re-runs18 integration/path-commit commands, verifies `next`/ES integration
contain the fixes and compares source bytes with the installed-input record.
No product files changed during the final qualification.

[QA20](../../qa-logs/2026-10-07-pixelelated-replacement-16/qa20-acceptance/acceptance.json)
passes all15 default suites,78walk frames with no unclaimed/missing/stale
differences,26actual retained-ROCKNIX-RC2 upgrade assertions,15direct identity
frames,4identical installed payload/proxy profiles and actual clean/upgraded
virgl plus upgraded software rendering. Saves, save states, settings, cloud
selection and archive survive the update. The exact emitted upgrade artifacts
are retained beside the acceptance receipt. Single timing samples measure
0.726s to first emulated frame,1.328s to completed exit sync and1.012s to the
next frame; these are not physical-device measurements or time to gameplay.

[Cloud02](../../qa-logs/2026-10-07-pixelelated-replacement-16/cloud02-acceptance/acceptance.json)
passes318 installed assertions:106each on actual owned WebDAV, SFTP and MinIO
S3, zero failures/skips. The installed rclone1.75.1 hash matches image16.
All three live backend identities and exact container/image identity were
observed; terminal process/container absence was independently verified.
This is not an authenticated hosted-provider or Dropbox test.

All final owners have four zero result channels, unchanged input seals and
verified actual process/guest/backend/port cleanup. Earlier failed fixtures
and product controls remain failed. The original installed matrix stays
84PASS/1FAIL; separate collision01 qualifies the corrected T23 with two
write-free refusals and a rejecting actual-old-script control. The completed
observer corrections #487/#488 change no product behavior or runtime verdict.

## PL-001 — Resolved on candidate16

Source repairs: `ed5a6a51f5974deec8748fbf0dbd2f4984b690f5` (discovery),
`ec2283f20f10e692f15bdb417917adb0e320155f` (legacy capability), with the
current ES pin above. [Independent matrix reconciliation](../../qa-logs/2026-10-07-pixelelated-replacement-16/matrix-primary-reconciliation/verification.json)
re-derives nine exact classifications, including unrelated/empty, actual
default fallback, explicit tiered/legacy root, stranded root and refused
listing. Supplemental02 proves supported membership on empty local libraries,
BIOS and unrelated-empty-directory controls without changing installed files.
The original unchanged14 content-probe/refutation failures and the actual15
false cannot-run frame remain the negative controls; legacy-support-host01
also executes the original wrong support label and corrected restore behavior.

Root/reasons640 and1280 retain20 EN/FR cases and88directly reviewed frames;
the real selected root shows supported Game Boy content. [Selected-content01](../../qa-logs/2026-10-07-pixelelated-replacement-16/selected-content01-acceptance/acceptance.json)
adds actual installed legacy/tiered/BIOS downloads with exact source/destination
hashes, unchanged source/config/pointers and a known unsupported-system flag0.
[Content-routing01](../../qa-logs/2026-10-07-pixelelated-replacement-16/content-routing01-acceptance/acceptance.json)
proves actual EN/FR640 automatic default fallback and successful manual
selection, with30direct frames, exact stored paths, fresh selection logs and
journals. Earlier UI04 ordinary-name flows retain their explicit source
continuity. QA20/cloud02 supply final clean/upgrade/protocol qualification.

Already written: existing content, unrelated folders and explicit/custom
selections are preserved. Discovery does not move cloud files. Only the normal
discovered-folder or manual-selection flow changes this device's content
pointer; actual restore downloads the selected original bytes. No fielded
Rasteratops migration gate is introduced.

## PL-003 — Resolved on candidate16

Final migration repair: `4b312e784f425947defd906a15650b5e0ec0f8ea`, including
the preceding historical-tier fix `ec2283f20f10e692f15bdb417917adb0e320155f`.
The installed two-guest matrix and independent readback retain the earlier
sibling's active saves/discarded-save shelf in all root/custom/current-content
cases while the current guest stays settled. Supplemental02 explicitly
refuses unreadable active-sibling listings, preserves all state and passes
repeated current scans after the fault is removed.

Inherited-shelf01 executes the actual RC2 writer and completes all four owned
tiers for complete/record-copy/record-delete histories, removes the record
and leaves repeated apply unchanged. Partial640-02 and1280-02 execute four
real EN/FR copies killed at258048/8391392bytes. Original bytes/pointers/record
survive, actual UI TRY AGAIN completes all originals, and the next backup
keeps displaced saves in current Saves-replaced. All32frames were directly
reviewed. The old failed UI retry and historical shelf omission remain
negative evidence; source controls retain22focused/398full passes, four
old-source expected failures and five old refusal controls. Final QA20 and
cloud02 pass without changing product files.

Already written: an earlier device deliberately keeping its layout retains
its active shelf. Actual interrupted RC2-owned history is recovered. A verified
partial destination is resumed only with its validated original recovery
record and exact source-prefix agreement; foreign, changed, extra, unreadable
or unrecorded data stays refused. No original data is discarded to clear a
failed move. The existing old parent may remain empty; it is compared directly,
not falsely required absent.

## PL-004 — Resolved on candidate16

Binding repair landed in `ed5a6a51f5974deec8748fbf0dbd2f4984b690f5`;
recovery presentation is retained in ES `8beab9090c73ccc47da49f29f31fa73584fc0877`
and `72494bc72e3d64d4dcfeb4e6478052bbdf166c5b`.
The installed matrix and raw-log reconciliation prove comment/format/token
rewrites, genuine changed-endpoint/root refusal and legacy-record recovery.
Both original witnesses recover exactly; the unrelated endpoint is unchanged.
Three actual state/scan/apply refusals name the original connection.

Recovery640/1280 executes the supported terminal configuration repair and real
UI retry in EN/FR, preserving original data, completing both tiers and removing
the record. Across all16 recovery/control cases,92frames were directly viewed.
The full French original-connection reason and complete `rclone config` / `E`
instruction fit both profiles. Real missing-folder/network controls remain
distinct. The prior installed comment-only refusal remains the negative
control. Full QA20/cloud02 now satisfy the remaining qualification boundary.

Already written: existing validated records retain their original cloud
binding and data. Harmless configuration formatting and token refresh do not
strand the move. A genuinely changed connection is not silently rebound;
restoring the original connection enables explicit, verified retry. No
partial source copy is deleted to manufacture a successful state.

## PL-005 — Resolved on candidate16

Typed scan reasons landed in `ed5a6a51f5974deec8748fbf0dbd2f4984b690f5`,
ES `bab4df649f48847cc43d21c77c058107ad902754`; full recovery text fits via
`8beab9090c73ccc47da49f29f31fa73584fc0877` and current72494.
Installed future/malformed layout, configuration-read and record-read
refusals emit the true reason and preserve cloud bytes and pointers.
Supplemental02 proves initial record-write and marker-write refusal/retry and
a real closed endpoint. Application failures do not enter the rclone-only
status mapper. Old missing-folder and generic-timeout outputs remain retained.

Root/reasons640/1280 and recovery640/1280 bind the actual English/French pages,
cards and terminal instruction to their runtime outcomes. Four stock outer
timeouts measure30.01seconds each, retain original state and retire the
provider/sleep children. The first two1280timeout captures in each language
show full text; the third records normal dismissal, not text-fit proof.
Missing-folder and network controls keep distinct reasons. All final default,
upgrade and protocol qualification is now accepted.

Already written: invalid/future markers, unreadable settings/records and
partial cloud state remain intact and safely refused. The repair changes the
reason and supported recovery guidance, not refusal into destructive fallback
or automatic folder creation.

## Final outcome boundary

All eight original punch items have command-backed resolved outcomes. None is
deferred or withdrawn. The frozen forward-audit grades remain historical;
09 maps later completion and the existing public-docs/account/licence/device
gates. This completes the software fixes audit. It does not designate an RC,
publish a release, prove physical hardware behavior or authorize broader
cleanup. Source/library custody carries unchanged earlier proofs explicitly;
no new RA award/reset or upstream-freshness query is claimed.
'''
with (a/'08-installed-resolution.md').open('a') as f:f.write('\n'+text)
s=(a/'05-punch-list.md').read_text()
s=s.replace('— open; remediation required.','— all eight outcomes resolved; tracker closure follows evidence publication.')
s=re.sub(r'^\*\*State:\*\*.*$', '**State:** Phase7 complete: all eight findings resolved on qualified candidate16. Evidence publication and exact tracker readback follow; no RC or publication claim.',s,flags=re.M)
start=s.index('PL-002/006/007/008 are resolved from landed source');end=s.index('| Item | Outcome',start)
s=s[:start]+'All eight findings are resolved from landed source and independently accepted\ninstalled proofs. Detailed command, state-preservation and final-qualification\nevidence is in [08-installed-resolution.md](08-installed-resolution.md).\n\n'+s[end:]
commits={'PL-001':'ec2283f20f10e692f15bdb417917adb0e320155f','PL-003':'4b312e784f425947defd906a15650b5e0ec0f8ea','PL-004':'ed5a6a51f5974deec8748fbf0dbd2f4984b690f5','PL-005':'ed5a6a51f5974deec8748fbf0dbd2f4984b690f5'}
for key,commit in commits.items():
    s=s.replace('| '+key+' | Open | Acceptance unproved on repaired bytes. |','| '+key+' | Resolved | Candidate16 `ee01490913`, final clean/actual RC2 upgrade and cloud318; [command-backed resolution](08-installed-resolution.md). |')
    start=s.index('- id: '+key);end=s.find('\n- id:',start+1)
    if end<0:end=s.index('\n```',start)
    block=s[start:end];assert '  outcome: open' in block
    block=block.replace('  outcome: open','  outcome: resolved\n  resolution_commit: "'+commit+'"\n  resolution_evidence: "08-installed-resolution.md; ../../qa-logs/2026-10-07-pixelelated-replacement-16/phase7-source-readback/final-acceptance-receipts.json"')
    s=s[:start]+block+s[end:]
s=s.replace('#467 (open).','#467 (acceptance complete; tracker closure follows publication).').replace('#468 (open).','#468 (acceptance complete; tracker closure follows publication).')
(a/'05-punch-list.md').write_text(s)
p=a/'07-remediation-progress.md';s=p.read_text();start=s.index('Current outcome index:');end=s.index('## Initial',start)
s=s[:start]+'Current outcome index: [08-installed-resolution.md](08-installed-resolution.md)\nrecords all eight findings resolved after candidate16 final qualification.\nThe dated entries below preserve historical intermediate states. No RC or\nrelease-publication claim is implied.\n\n'+s[end:];p.write_text(s)
with (a/'00-running-log.md').open('a') as f:f.write('\n## '+stamp+' — Phase7 all eight outcomes resolved\n\n'+
'Final QA20/cloud02, selected-content01 and direct content-routing01 acceptance\nare complete. Re-derived integration/path commits and all original-state\ndispositions are in08; the05table and YAML record eight resolved outcomes.\nOriginal failed runs and frozen forward-audit grades remain unchanged. Next:\nresolution lint, ordinary evidence publication, exact issue/body readbacks,\nthen #461 capacity and H700 arm/aarch64 qualification. No further external\nmodel call, personal account action, physical test or release is authorized.\n')
print('Recorded all eight outcomes with gated final acceptance; run resolution lint next')
