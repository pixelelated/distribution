from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,shutil
old=Path('/workspace/tmp/pixelelated-m7-p4-build16-installed-matrix-01')
owner=old.with_name('pixelelated-m7-p4-build16-collision-01')
assert not owner.exists();owner.mkdir(mode=0o700);(owner/'proof').mkdir(mode=0o700)
for name in ['run.py','verify-inputs.py']:
 text=(old/name).read_text().replace(old.name,owner.name)
 if name=='run.py':
  text=text.replace('reader-value-control.py','collision-control.py')
  text=text.replace("'--output',str(owner/'proof')", "'--output',str(owner/'proof'),'--case','T23-content-collision'")
 ast.parse(text);(owner/name).write_text(text)
source=Path('tools/pixelelated-vm-cloud-boundaries')
shutil.copy2(source,owner/'boundaries.py')
control='''from pathlib import Path
import hashlib,importlib.machinery,importlib.util,json,subprocess
owner=Path(__file__).resolve().parent
loader=importlib.machinery.SourceFileLoader('collision_boundaries',str(owner/'boundaries.py'))
spec=importlib.util.spec_from_loader(loader.name,loader);m=importlib.util.module_from_spec(spec);loader.exec_module(m)
original=m.Proof.collision
def collision(self):
 original(self)
 self.reset()
 self.put('ROCKNIX/Saves/gb/A.srm',b'local progress\\n')
 self.put('ROCKNIX/Content/ROMs/gb/A.gb',b'old content\\n')
 self.put('pixelelated/Content/ROMs/gb/A.gb',b'foreign content\\n')
 before=self.audit_snapshot()
 ref='ed5a6a51f5974deec8748fbf0dbd2f4984b690f5'
 old=subprocess.check_output(['git','-C',str(self.tree),'show',ref+':'+m.SOURCES+'/cloud_migrate_layout'])
 path=m.QA+'/pre-fix-cloud-migrate-layout'
 self.on('a','cat > '+path+'; chmod 755 '+path,data=old.decode())
 result=self.on('a',path+' --apply',allowed=None)
 after=self.audit_snapshot()
 record=self.on('a','test -s /storage/.config/cloud-layout-migration.json',allowed=None).returncode==0
 m.require(result.returncode!=0 and '>>> why THE NEW FOLDER ALREADY HAS FILES IN IT' in result.stdout,'old control did not reach the intended collision refusal')
 preserved=after==before and not record
 m.require(not preserved,'actual old script unexpectedly meets the stronger refusal invariant')
 m.require(record and after['cloud']!=before['cloud'],'old refusal must reproduce partial tier advancement and a created record')
 m.require(set(before['cloud'].values()).issubset(set(after['cloud'].values())),'old control lost original bytes')
 m.require((self.data/'pixelelated/Content/ROMs/gb/A.gb').read_bytes()==b'foreign content\\n','old control overwrote foreign content')
 m.save(self.logs/'old-collision-negative-control.json',{'ref':ref,'source_sha256':hashlib.sha256(old).hexdigest(),'returncode':result.returncode,'before':before,'after':after,'record_created':record,'stronger_invariant':preserved,'scope':'Actual predecessor script in private guest QA path; installed binaries unchanged.'})
 print('PASS actual predecessor collision refusal rejected by unchanged-state predicate',flush=True)
 self.reset()
m.Proof.collision=collision
raise SystemExit(m.main())
'''
ast.parse(control);(owner/'collision-control.py').write_text(control)
manifest=Path('/workspace/tmp/pixelelated-m7-replacement-16/inputs.json');j=json.loads(manifest.read_text());tree=Path(j['host_worktree'])
(owner/'provenance.json').write_text(json.dumps({'prepared_utc':datetime.now(timezone.utc).isoformat(),'parent':str(old),'issue':485,
 'candidate':j['distribution_commit'],'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),
 'harness_change':'Only T23 now requires two write-free refusals with no recovery record. All frozen product and original207 QA inputs remain unchanged; the corrected observer is separately sealed.',
 'scope':'One failed case requalified; original84 passing cases remain the original matrix evidence. Actual predecessor source is a negative control, not an old installed image.'},indent=2)+'\n')
files=sorted(p for p in owner.iterdir() if p.is_file())+[tree/name for name in j['qa_source_files']]
(owner/'seal.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
print(owner)
