#!/usr/bin/env python3
"""Read only named source/compact receipt members; no evidence helper execution."""
from pathlib import Path
import hashlib,json,subprocess,tarfile,difflib
R=Path('/workspace/repos/rocknix.worktrees/m7-player-setup')
O=Path(__file__).resolve().parent
REF='cdd92f10605517e789e09d13b6f4ba68573c2617'
rows=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def put(n,b,source,**kw):
 assert len(b)<=2*1024**2
 p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 rows.append(dict(retained=n,source=source,bytes=len(b),sha256=sha(b),**kw));return b
def file(n,p):
 p=Path(p);return put(n,p.read_bytes(),str(p))
def git(n,p,ref=REF):
 b=subprocess.check_output(['git','-C',str(R),'show',ref+':'+p]);return put(n,b,'git:'+ref+':'+p)
def member(n,a,m):
 p=R/a;assert p.stat().st_size<2*1024**2
 with tarfile.open(p) as t:
  info=t.getmember(m);assert info.isfile() and info.size<2*1024**2;b=t.extractfile(info).read()
 return put(n,b,str(p)+'::'+m,archive_sha256=sha(p.read_bytes()))
def data(n,j,source):return put(n,(json.dumps(j,indent=2)+'\n').encode(),source,derived=True)
base='docs/qa-logs/2026-10-15-qualification-followups/baseline-correction.tar.gz'
for n in ['evidence/qa20-final-result.json','evidence/qa20-first-run.py','last-good-scripts-test.diff','run.py']:
 member('baseline/'+n,base,'baseline-correction/'+n)
for n in ['config.json','result.json','host-exits.json','consumption-draft.json','webdav/report.md']:
 file('baseline/'+n,R/'docs/qa-logs/2026-10-15-baseline-continuation'/n)
owner=Path('/workspace/tmp/pix-m7-final-baseline-20261014-03')
comparison={n:sha((owner/n).read_bytes())==sha((O/'baseline'/n).read_bytes()) for n in ['config.json','result.json','run.py']}
old=(Path('/tmp/pix-m7-baseline-harness-correction-20261015/original/last-good-scripts-test')).read_bytes()
new=subprocess.check_output(['git','-C',str(R),'show',REF+':tools/last-good-scripts-test'])
prior=subprocess.check_output(['git','-C',str(R),'show','1a026648442321609b2288c2c9c06803817f9df2:tools/last-good-scripts-test'])
delta=''.join(difflib.unified_diff(old.decode().splitlines(True),new.decode().splitlines(True),fromfile='retained-ebd9a466',tofile='frozen-cdd92'))
put('baseline/original-to-frozen.diff',delta.encode(),'computed exact byte diff; no patch application/execution',derived=True)
rc=subprocess.run(['git','-C',str(R),'merge-base','--is-ancestor','1a026648442321609b2288c2c9c06803817f9df2',REF]).returncode
data('baseline/binding-check.json',dict(ancestor_command=['git','merge-base','--is-ancestor','1a026648442321609b2288c2c9c06803817f9df2',REF],original_exit=rc,prior_commit_tool_sha256=sha(prior),historical_retained_tool_sha256=sha(old),frozen_tool_sha256=sha(new),actual_owner_vs_compact=comparison,actual_owner=str(owner),actual_run=(owner/'run.path').read_text().strip()),'exact named Git objects and original owner files')
git('frozen/readiness.md','docs/releases/next-candidate-work.md')
git('frozen/steam-package.mk','projects/ROCKNIX/packages/emulators/standalone/steam/package.mk')
git('frozen/vm-qa','tools/vm-qa')
claims=git('frames/claims.txt','tools/vm-walks/claims.txt')
original=member('frames/claims.composed.txt','docs/qa-logs/2026-10-15-frame-claims/original-packet.tar.gz','packet/claims.composed.txt')
for n in ['review.txt','README.md','proposed-578-background-regions.json','handoff-hashes.json']:
 file('frames/'+n,R/'docs/qa-logs/2026-10-15-frame-claims'/n)
member('frames/execution-result.json','docs/qa-logs/2026-10-15-frame-claims/original-packet.tar.gz','packet/execution01/result.json')
p=R/'docs/qa-logs/2026-10-15-frame-claims/pixel-inventory.json';b=p.read_bytes();j=json.loads(b)
projection=[{k:v for k,v in f.items() if k!='row_spans'} for f in j['frames']]
live=[(i,l) for i,l in enumerate(claims.decode().splitlines(),1) if l.strip() and not l.startswith('#')]
data('frames/pixel-summary.json',dict(original=str(p),original_sha256=sha(b),original_bytes=len(b),scope='metadata projection; no pixel comparison rerun',frames=projection,all78_outside_support_zero=all(f['outside_carousel_change_support']==0 for f in j['frames']),original_residual_pixels=sum(f['outside_existing_masks_and_claims'] for f in j['frames']),claims_byte_equal=claims==original,claim_rows=len(live),claim_heads=sorted(set(l.split()[0] for i,l in live)),new_578_rows=sum('#578' in l for i,l in live)),'projection of existing published pixel inventory')
paths='projects/ROCKNIX/packages/virtual/emulators/sources/Install Steam.sh'
blocks=[]
for label,ref in [('old','07a16c4d2f3cb923e171c0f6b8dd43aafc4282b2'),('frozen',REF)]:
 b=git('steam/'+label+'-Install-Steam.sh',paths,ref);ls=b.splitlines(True)
 for tag in ['PY_STEAM_ROOT','PY_STEAM_FEX','PY_STEAM_RUNTIME','PY_PROTON_VARIANT']:
  start=next(i for i,l in enumerate(ls) if b"<<'"+tag.encode()+b"'" in l)
  end=next(i for i in range(start+1,len(ls)) if ls[i].strip()==tag.encode())
  part=b''.join(ls[start+1:end]);blocks.append(dict(source=label,commit=ref,module_sha256=sha(b),tag=tag,first_body_line=start+2,last_body_line=end,bytes=len(part),sha256=sha(part)))
data('steam/heredoc-bindings.json',blocks,'exact newline-preserving extraction between literal heredoc delimiters; no execution')
steam='docs/qa-logs/2026-10-13-library-vm/results/steam-results/compact-receipts.tar.gz'
for c in ['runtime','proton','root']:
 member('steam/'+c+'-result.json',steam,c+'/tmp/cases/result.json')
recovery=[]
for c in ['kill-staging','kill-old-renamed','kill-new-renamed','kill-first-link','kill-second-link','kill-committed','recovery-failure','cleanup-failure']:
 values={}
 for n in ['before.json','after-first.json','after.json','retry.log']:
  b=member('runtime-recovery/'+c+'/'+n,steam,'runtime/tmp/cases/'+c+'/'+n)
  if n.endswith('.json'):values[n]=json.loads(b)
  else:log=b.decode()
 recovery.append(dict(case=c,before_equals_after=values['before.json']==values['after.json'],after_first_equals_after=values['after-first.json']==values['after.json'],retry_reached_injected_wget9='returned non-zero exit status 9' in log,recovery_attention_message='Runtime recovery needs attention' in log,retry_original_exit1='OWNER_EXIT 1' in log))
data('runtime-recovery/comparison.json',recovery,'comparison of retained manifest dictionaries and original retry logs')
for n in ['guest-wifi-observer.py','guest_helpers.py']:
 member('wifi/'+n,'docs/qa-logs/2026-10-15-final-engineering-result/affected-source.tar.gz','affected/'+n)
for run in ['final-clean','final-retained']:
 for n in ['result.json','before-cleanup.json','owner-result.json','frontend.stderr','frontend.stdout']:
  file('wifi/'+run+'/'+n,Path('/tmp/pix-m7-audit603-20261015/extracted')/run/'wifi-candidate'/n)
sm=Path('/workspace/tmp/pix-m7-sm8550-refresh-20261015-02')
for n in ['preparation.json','launcher-submission.json','launcher-start.json','build.py','inside-build.sh']:
 file('sm/'+n,sm/n)
b=(sm/'inputs.json').read_bytes();j=json.loads(b)
data('sm/inputs-projection.json',dict(original=str(sm/'inputs.json'),original_sha256=sha(b),original_bytes=len(b),fields={k:j[k] for k in ['build_identity_set','build_timestamp','distribution_commit','frozen_at','host_worktree','container_name']}),'bounded selected fields of original inputs.json')
file('sm/prepare-owner.py','/tmp/pix-m7-sm8550-abl-retry-20261015/prepare-owner.py')
file('sm/acceptance.json','/tmp/pix-m7-audit603-20261015/extracted/abl-accepted/owner/acceptance/artifacts/acceptance.json')
file('sm/affected-products-staged.json','/workspace/tmp/pix-m7-sm8550-reader-20261015-01/artifacts/affected-products-staged.json')
file('sm/archive-reader-result.json','/tmp/pix-m7-audit603-20261015/extracted/checksum/archive-reader/result.json')
file('sm/verify-additions.py','/tmp/pix-m7-audit603-20261015/extracted/abl-accepted/owner/verify-additions.py')
for n in ['invocation.json','stdout','stderr']:
 p=R/'docs/audits/2026_10_15-milestone-603-completed-handoff/checks/pkgcheck-current'/n
 if p.exists():file('pkgcheck/'+n,p)
git('pkgcheck/package.mk','projects/ROCKNIX/packages/tools/rocknix-abl/package.mk')
git('pkgcheck/pkgcheck','tools/pkgcheck')
file('h700/installed-inclusion.json','/workspace/tmp/pix-m7-zerotier-h700-readback-20261015-01/artifacts/installed-inclusion.json')
(O/'evidence-index.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(dict(files=len(rows),retained_bytes=sum(x['bytes'] for x in rows),no_runtime_or_provider_execution=True)))
