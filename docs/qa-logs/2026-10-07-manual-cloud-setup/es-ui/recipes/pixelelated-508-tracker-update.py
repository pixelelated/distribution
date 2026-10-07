import json,subprocess
from pathlib import Path
repo='repos/pixelelated/distribution'
def read(path):return json.loads(subprocess.check_output(['gh','api',repo+path],text=True))
def patch(path,data,name):
 p=Path('/tmp')/name;p.write_text(json.dumps(data));subprocess.run(['gh','api','--method','PATCH',repo+path,'--input',str(p)],check=True,stdout=subprocess.DEVNULL)
 d=read(path)
 for k,v in data.items():assert d[k]==v,(path,k)
 print(path,'verified')
d=read('/issues/505')
head='## Disposition — replaced by manual cloud setup (#508)'
assert head not in d['body']
body=d['body']+'\n'+head+'\n\nThe maintainer explicitly approved the reviewed patch and VM tests, then chose to abandon cloud-folder migration in favor of ordinary backend linking, folder creation and manual population. The exact approved patch is applied only in the isolated feature/m7-migration-diagnostics tree; it was not integrated, pushed or VM-tested. All earlier scratch jobs are terminal. Do not resume the retired migration-specific diagnostics or new reassurance copy; #508 owns coordinated script/UI removal and focused regression proof. The unchecked criteria above are historical, not completed. Closing as not planned, not as a fixed diagnostics implementation. Private host Dropbox reconciliation remains separate, with no rename/deletion performed.\n'
patch('/issues/505',{'body':body,'state':'closed','state_reason':'not_planned'},'pixelelated-505-disposition.json')
d=read('/milestones/7');old=d['description'];s=old
s=s.replace('## Current priority — accepted device artifacts; diagnostics, delta review and release gates','## Current priority — manual cloud setup, delta review and release gates')
marker='P3 GENERIC_X64 qualification and P4 fixes audit are complete on candidate16.'
assert marker in s
s=s.replace(marker,'**Now: #508 replaces automatic cloud-folder migration with ordinary linking, folder creation and explicit selection (D-CLOUD-175).** Fresh configurations use /pixelelated; existing credentials and configured paths remain until explicitly changed. Users populate or rearrange the cloud themselves. #505 is closed not planned; its applied draft stays isolated and unintegrated. Prove the coordinated script/UI replacement on synthetic VMs, freeze it for #507, then bind it into selected release firmware. The owner’s Dropbox recovery is a separate host-side inventory/reconciliation, with no rename/delete inferred.\n\n'+marker,1)
a='#505 has a fresh isolated feature worktree and a bounded diagnostic proposal.'
i=s.index(a);j=s.index('After diagnostic proof,',i)
s=s[:i]+'The maintainer later approved #505, then replaced the migration approach entirely under #508/D-CLOUD-175. Keep existing credentials and selected paths; fresh linking seeds /pixelelated, explicit folder selection changes pointers, and no automatic join/follow/move remains. #505\'s diagnostic patch stays isolated and unintegrated, with its issue closed not planned. Host Dropbox inventory and any later named reconciliation action remain private and separate. '+s[j:]
s=s.replace('After diagnostic proof, freeze','After #508\'s focused script/UI proof, freeze')
s=s.replace('diagnostics#505','#508 manual setup').replace('diagnostics #505','#508 manual setup')
patch('/milestones/7',{'description':s},'pixelelated-m7-manual-plan.json')
