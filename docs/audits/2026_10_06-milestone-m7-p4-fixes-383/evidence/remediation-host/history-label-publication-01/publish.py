from pathlib import Path
import datetime,hashlib,json,subprocess
repo=Path('/workspace/repos/rocknix.worktrees/conflict-resolution');primary=Path('/workspace/repos/rocknix');prefix=Path('/tmp/pixelelated-m7-history-label')
def git(where,*args):return subprocess.check_output(['git','-C',str(where),*args],text=True).strip()
assert git(primary,'branch','--show-current')=='next' and not git(primary,'status','--porcelain')
assert git(repo,'branch','--show-current')=='feature/conflict-resolution'
assert not git(repo,"diff","--cached","--name-only")
paths=['.github/sessions/saved-session-state-next.md', 'docs/audits/2026_10_06-milestone-m7-p4-fixes-383', 'docs/qa-logs/2026-10-06-pixelelated-replacement-15', 'docs/friction-log.md', 'docs/work-logs/2026_10-work_logs/2026_10_06-work_log.md', 'docs/work-logs/INDEX.md', 'docs/cloud-sync-changelog.md', 'docs/rasteratops/release-readiness.md', 'projects/ROCKNIX/packages/network/rclone/sources/cloud_migrate_layout', 'projects/ROCKNIX/packages/network/rclone/sources/cloud_content_restore', 'tools/rasteratops-cloud-layout-test']
subprocess.run(['git','-C',str(repo),'add','--',*paths],check=True)
changed=git(repo,'diff','--cached','--name-only').splitlines();assert changed and all(p.startswith(('docs/', '.github/sessions/')) or p in paths for p in changed)
def operation(label,where,*args):
 with Path(str(prefix)+'-'+label+'.log').open('x') as log:
  result=subprocess.run(['git','-C',str(where),*args],stdout=log,stderr=subprocess.STDOUT)
 assert result.returncode==0,label+' failed; read retained log'
 print(label+' completed',flush=True)
operation('commit',repo,'commit','-F','/tmp/pixelelated-m7-history-label-message.txt')
feature=git(repo,'rev-parse','HEAD')
operation('integration',primary,'cherry-pick','-x',feature)
next_sha=git(primary,'rev-parse','HEAD')
operation('push-feature',repo,'push','origin','HEAD:feature/conflict-resolution')
operation('push-next',primary,'push','origin','next')
remotes={}
for where,branch,sha in [(repo,'feature/conflict-resolution',feature),(primary,'next',next_sha)]:
 actual=git(where,'ls-remote','origin','refs/heads/'+branch).split()[0];assert actual==sha,(branch,actual,sha);remotes[branch]=actual
for p in changed:assert git(repo,'rev-parse',feature+':'+p)==git(primary,'rev-parse',next_sha+':'+p),p
receipt={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'feature':feature,'next':next_sha,'remote_refs':remotes,'changed_paths_equal':changed,'scope':'normal hooked commit/cherry-pick-x/push; equality only for changed paths; tested history/capability source repair; frozen candidate15 unchanged; installed16 acceptance pending','hosted_step':'verified SUCCESS; #472 closed; separate audit cadence remains open'}
dest=repo/'docs/audits/2026_10_06-milestone-m7-p4-fixes-383/evidence/remediation-host';(dest/'history-label-publication.json').write_text(json.dumps(receipt,indent=2)+'\n')
(dest/'sha256.json').write_text(json.dumps({str(p.relative_to(dest)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(dest.rglob('*')) if p.is_file() and p.name!='sha256.json'},indent=2)+'\n')
print(json.dumps({'feature':feature,'next':next_sha,'verified_utc':receipt['verified_utc'],'changed_paths':len(changed)}),flush=True)
