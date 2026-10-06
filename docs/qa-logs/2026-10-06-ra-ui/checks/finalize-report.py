from pathlib import Path
import hashlib,json,datetime
base=Path('/workspace/repos/rocknix.worktrees/conflict-resolution/docs/qa-logs/2026-10-06-ra-ui')
q=base/'qualified-03';completion=json.loads((q/'completion.json').read_text())
assert completion['assertions']==109 and set(completion['result_channels'].values())=={0}
review=json.loads((base/'visual-review.json').read_text())
frames={str(p.relative_to(base)) for p in (q/'artifacts').glob('*/*.png')}
assert len(frames)==23 and {r['path'] for r in review['frames']}==frames
for r in review['frames']:
 assert r['passed'] and hashlib.sha256((base/r['path']).read_bytes()).hexdigest()==r['sha256']
profiles=[];identity=None
for d in sorted((q/'artifacts').glob('*')):
 if not d.is_dir():continue
 results=json.loads((d/'result.json').read_text());assert results['failures']==0
 assertions=json.loads((d/'assertions.json').read_text());assert len(assertions)==results['assertions'] and all(r['passed'] for r in assertions)
 before=(d/'installed-before.sha256').read_bytes();after=(d/'installed-after.sha256').read_bytes()
 assert before==after and len(before.splitlines())==46
 if identity is None:identity=before
 assert identity==before
 assert (d/'es-before.txt').read_bytes()==(d/'es-after.txt').read_bytes()
 assert results['source_sha256']==hashlib.sha256((q/'harness/ra-ui-test').read_bytes()).hexdigest()
 accepted=json.loads((d/'accept-flush.json').read_text());assert accepted['outcome']['flushed']==1 and accepted['outcome']['pending_remaining']==0
 assert (d/'accept-stamp.txt').read_text().split()[1:]==['0','sent']
 profiles.append({'profile':d.name,'assertions':len(assertions),'frames':len(list(d.glob('*.png'))),'passed':True})
r=json.loads((q/'artifacts/en_US-640x480/refuse-flush.json').read_text());assert r['outcome']['flushed']==0 and r['outcome']['pending_remaining']==1
assert any(v['action']=='awardachievement' and v['status']==503 for v in r['requests'])
assert (q/'artifacts/en_US-640x480/refuse-stamp.txt').read_text().split()[1:3]==['5','not-sent']
record={'qualified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':'7afa9efcfc0c1ce4b89774b38878fc1b9a9063d2','candidate_bundle':'b77e47e57a4bb35f885ba78669ee8176a9ac978b27c1cbcfaad66e18f684a9f1','assertions':109,'failures':0,'skips':0,'frames_directly_reviewed':23,'profiles':profiles,'installed_file_hashes_per_profile':46,'same_installed_hashes_all_profiles':True,'all_four_results_zero':True,'actual_cleanup_verified_utc':completion['verified_utc'],'boundary':'Synthetic local award/HTTP provider; installed ES/ctl/Storage/flusher. Real provider award remains separate RA33. No whole changed ordinary-runner rerun.'}
(base/'qualification.json').write_text(json.dumps(record,indent=2)+'\n')
p=base/'README.md';s=p.read_text();s=s.replace('Owner03 adds explicit\nprofile-store isolation and must pass before the P4 audit begins.','Owner03 adds explicit\nprofile-store isolation and supplies the final qualified matrix below.')
s+='''
## Qualified owner03

**109 PASS, 0 FAIL, 0 SKIP; all23 original frames directly reviewed.**
English640 has34 assertions (including refusal); each other profile has25.
Every baseline is empty, every sending/sent card is readable without clipping,
and dismissal/empty-repeat frames show no notification. Installed ES/ctl and
all44 proxy files have identical hashes across all four profiles and before/
after each run. Each profile keeps the same restarted ES PID/start ticks.

Owner `/workspace/tmp/pixelelated-m7-ra-ui-03`, run20261006T065301Z-41c3ed1c.
All four result channels are0; `qualified-03/completion.json` records terminal
status and actual launcher/job/watcher/two-guest process absence, no QEMU and
unbound10026/5912. The local provider/flusher exits are checked inside every
profile. The source, candidate and sealed harness verify before/after.

`visual-review.json` binds every inspected frame to its SHA256; the unmodified
per-profile result files deliberately retain visual_review=pending because
visual inspection is a later separate gate. `qualification.json` combines
that gate with the assertions and actual cleanup. Prior attempts remain
superseded. This closes #465's UI proof; P4 is the next gate, not a completed
audit or RC/device-ready claim.
'''
p.write_text(s)
print(json.dumps(record,indent=2))
