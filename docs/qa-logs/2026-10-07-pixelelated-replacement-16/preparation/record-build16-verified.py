from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil

repo = Path.cwd()
q = repo / 'docs/qa-logs/2026-10-07-pixelelated-replacement-16'
base = Path('/workspace/tmp')
now = datetime.now(timezone.utc)
for owner_name, target, receipt in [
    ('pixelelated-m7-replacement-16', 'build-completed', 'completion.json'),
    ('pixelelated-m7-store-16', 'store-completed', 'owner-verification.json'),
    ('pixelelated-m7-image-16', 'image-completed', 'owner-verification.json'),
]:
    owner = base / owner_name
    assert json.loads((owner / receipt).read_text())['result'] == 'PASS'
    dest = q / target
    dest.mkdir()
    names = [receipt, 'inner.rc', 'outer.rc', 'tool-wrapper.rc', 'launcher-result.json',
             'console.log', 'run.path', 'harness.sha256', 'bundle.path', 'container-observed.json']
    for name in names:
        if (owner / name).is_file():
            shutil.copy2(owner / name, dest / name)
    if target == 'image-completed':
        shutil.copytree(owner / 'artifacts', dest / 'artifacts')
    runfile = owner / 'run.path'
    if not runfile.exists():
        runfile = owner / 'build.run'
    if runfile.exists():
        run = Path(runfile.read_text().strip())
        if not run.is_absolute():
            run = Path('/workspace/repos/rocknix.worktrees/m7-pixelelated-replacement16') / run
        assert run.is_dir(), str(run)
        (dest / 'watcher').mkdir()
        for name in ['build.rc', 'build.status', 'build.pid', 'watcher.pid', 'command.pid', 'job.json', 'result.json']:
            if (run / name).is_file():
                shutil.copy2(run / name, dest / 'watcher' / name)
    (dest / 'sha256.json').write_text(json.dumps({str(p.relative_to(dest)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(dest.rglob('*')) if p.is_file()}, indent=2) + '\n')

status = f'''## Current execution — {now:%Y-%m-%d %H:%M} UTC

Both approved Fable audit calls and grading are complete. Phase 7 remains open:
PL-002/006/007/008 are resolved; PL-001/003/004/005 await candidate 16 installed
acceptance in #471. The interruption-copy refinement #482 is included at ES
`72494bc72e3d64d4dcfeb4e6478052bbdf166c5b`.

Candidate 16 built successfully: 642/642 tasks, all four result channels zero,
source/input seals verified, and its container and worker processes exited.
Distribution: `ee014909137e03706e0b3020b8396be589aaa705`.
Immutable bundle: `7f98f2d22985d11fe9c150015457894caf460104c9ce44abd16074167f23815a`.
Disk-image and update SYSTEM payloads are byte-identical:
`5767ee7d72f3c538259ee927ad681c63533d661997b64e6beac9d83fdc70812c`.
Primary verification completed at 00:25:38 (build), 00:26:39 (store), and
00:28:45 (image extraction). These checks do not establish VM acceptance.

The 85-case installed matrix started at 00:28:54 under
`/workspace/tmp/pixelelated-m7-p4-build16-installed-matrix-01`, launcher 57723,
watcher 57725, run `20261007T002854Z-d1d7980f`. Two isolated QA guests are running.
The primary actively consumes the watcher result; disconnected alerts remain #395.

The exact approved two-disk retirement is complete: 10,713,485,312 bytes recovered,
all other evidence and protected sources preserved. No broader cleanup or reserve
change was made or is authorized. The fixed swap helper passed before the build.

**Next:** installed matrix → historical shelf and actual interrupted-file UI retry /
next-backup preservation → English/French recovery/reason/interruption frames at
640×480 and 1280×800 → full clean/actual RC2-upgrade QA20 and final artifact scans →
#471/P4 closure → #461 device capacity review → H700 DDR4 RG35XX SP arm, then
aarch64 → named physical/P5 gates. #478/#479/#482 remain open until acceptance.
No new RA reset or Dropbox credential is needed. Ten #168 upstream drafts remain
unsubmitted. No release-candidate designation or device-readiness claim yet.

Evidence: `docs/qa-logs/2026-10-07-pixelelated-replacement-16/`; source and earlier
results: `docs/audits/2026_10_06-milestone-m7-p4-fixes-383/`.
'''
(repo / '.build-runs/build16-current.md').write_text(status)
for path in [q / 'README.md', repo / 'docs/rasteratops/release-readiness.md', repo / '.github/sessions/saved-session-state-next.md']:
    text = path.read_text()
    start = text.index('## Current execution')
    endmark = '`docs/audits/2026_10_06-milestone-m7-p4-fixes-383/`.\n'
    end = text.index(endmark, start) + len(endmark)
    path.write_text(text[:start] + status + text[end:])
with (repo / 'docs/work-logs/2026_10-work_logs/2026_10_07-work_log.md').open('a') as f:
    f.write(f'\n\n## {now:%H:%M} UTC — #471 candidate 16 built and payload verified; installed matrix active\n\n' + status.split('\n\n', 1)[1])
for name in ['00-running-log.md', '07-remediation-progress.md']:
    with (repo / 'docs/audits/2026_10_06-milestone-m7-p4-fixes-383' / name).open('a') as f:
        f.write('\n\n' + status)
print('Retained completed build, bundle and image receipts; recorded active installed matrix.')
