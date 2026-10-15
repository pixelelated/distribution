from pathlib import Path
import subprocess,json,datetime
R=Path('/workspace/repos/rocknix');C=Path('/workspace/repos/rocknix.worktrees/m7-player-setup');out=Path('/tmp/pix-m7-audit603-integration-correction-20261015');out.mkdir()
def git(*args,input=None,cwd=R):
 p=subprocess.run(['git',*args],cwd=cwd,input=input,capture_output=True);assert p.returncode==0,p.stderr.decode();return p.stdout.decode().strip()
old=git('rev-parse','next');assert old=='ddb9edb7363b9629cb9d22e5c784ceb409a9acd4';assert not git('status','--porcelain') and not git('status','--porcelain',cwd=C)
base=git('rev-parse','9b4d1dde53^');seq=git('rev-list','--reverse',base+'..'+old).splitlines();assert len(seq)==4
remote=git('ls-remote','origin','refs/heads/next').split()[0];assert remote=='62c382f46732bd0b69782d23c3e5417bd02c2258';assert git('rev-parse','origin/next')==remote
parent=base;mapping=[]
for orig in seq:
 tree=git('rev-parse',orig+'^{tree}');parents=git('show','-s','--format=%P',orig).split();assert len(parents)==1
 message=git('show','-s','--format=%B',orig)
 if orig.startswith('9b4d1dde53'):message+='\n\nRefs #606 and #603. Retain the original failed keyboard proof and audit record resolution.'
 new=git('commit-tree',tree,'-p',parent,input=(message+'\n').encode());assert git('rev-parse',new+'^{tree}')==tree
 mapping.append({'original':orig,'integration':new,'tree':tree,'message_changed':orig.startswith('9b4d1dde53')});parent=new
assert git('rev-parse',parent+'^{tree}')==git('rev-parse',old+'^{tree}')
git('update-ref','refs/heads/feature/m7-audit-integration-603',parent,'0'*40)
git('update-ref','refs/heads/next',parent,old)
assert not git('status','--porcelain')
git('switch','feature/m7-audit-integration-603',cwd=C);assert not git('status','--porcelain',cwd=C)
receipt={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reason':'pre-push refused unpublished next because original9b4d checkpoint lacked issue citation','remote_next_before':remote,'preserved_published_feature':'feature/m7-final-qualification-02','preserved_feature_head':old,'integration_branch':'feature/m7-audit-integration-603','local_next':parent,'identical_final_tree':git('rev-parse',parent+'^{tree}'),'mapping':mapping,'force_push':False,'product_bytes_changed':False}
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
